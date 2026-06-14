import json
import re

import anthropic

from agents.message_bus import MessageBus
from knowledge_base.store import KBStore

_MAX_TOOL_ITERATIONS = 12

SEARCH_KB_TOOL = {
    "name": "search_knowledge_base",
    "description": "Search the project's uploaded knowledge base documents for relevant excerpts. Use this to ground your work in the user's own data.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to look for in the knowledge base"}
        },
        "required": ["query"],
    },
}


class SingleAgentLoop:
    """Autonomous single-agent loop (claude-code style): one agent follows a Markdown
    instruction document.

    Two phases keep the deliverable clean:
    1. Research loop — the agent calls tools (knowledge base + web) and reasons. Its text
       is treated as thinking, NOT as the final answer, and is surfaced live as "thoughts".
    2. Finalize — a dedicated, streamed call that returns ONLY the deliverable in the exact
       required format (raw Markdown, or slide JSON), with no preamble or code fences.
    """

    def __init__(
        self,
        system_prompt: str,
        client: anthropic.AsyncAnthropic,
        run_id: int,
        bus: MessageBus,
        report_id: int,
        model: str = "claude-sonnet-4-6",
        internet_access: bool = False,
        output_mode: str = "markdown",
    ) -> None:
        self.system_prompt = system_prompt
        self.client = client
        self.run_id = run_id
        self.bus = bus
        self.report_id = report_id
        self.model = model
        self.internet_access = internet_access
        self.output_mode = output_mode

    def _tools(self) -> list[dict]:
        from agents.tools import WEB_TOOLS

        tools = [SEARCH_KB_TOOL]
        if self.internet_access:
            tools = tools + WEB_TOOLS
        return tools

    def _deliverable_kind(self) -> str:
        return "single presentation slide" if self.output_mode == "pptx" else "report section"

    def _research_message(self, instructions: str, chapter_title: str, chapter_description: str) -> str:
        return (
            f"# Instruction document\n\n{instructions}\n\n"
            f"---\n\n"
            f'Chapter context — title: "{chapter_title}"\n'
            f"Chapter description: {chapter_description or '(none)'}\n\n"
            f"You are preparing a {self._deliverable_kind()} for this chapter.\n"
            "STEP 1 — RESEARCH ONLY. Use your tools (search_knowledge_base, and web search if available) "
            "to gather the facts, figures and context you need. Think step by step and note what you find.\n"
            "Do NOT write the final deliverable yet — you will be asked to produce it in the next step. "
            "When you have gathered enough information, say briefly that you are ready."
        )

    def _final_instruction(self, chapter_title: str) -> str:
        if self.output_mode == "pptx":
            return (
                "STEP 2 — PRODUCE THE DELIVERABLE NOW. Based only on the research above and the instruction document, "
                "output the final slide.\n"
                "Output ONLY a single JSON object, nothing else — no preamble, no explanation, no ```json code fences:\n"
                '{"title": "A concise, impactful slide title (max 10 words)", '
                '"bullets": ["First key point", "Second key point", "Third key point"]}\n'
                "Rules: 4 to 7 bullets, each under 15 words, concrete facts and figures, no prose paragraphs."
            )
        return (
            "STEP 2 — PRODUCE THE DELIVERABLE NOW. Based only on the research above and the instruction document, "
            "write the final report section.\n"
            "Output ONLY raw Markdown — no preamble, no commentary, no JSON, no code fences. "
            f"Start directly with the chapter heading (e.g. # {chapter_title}). "
            "Use headers, bullet points and tables where appropriate, and include specific data points from your research."
        )

    async def run(self, instructions: str, chapter_title: str, chapter_description: str) -> str:
        from agents.orchestrator import _check_cancelled
        from agents.tools import execute_tool

        messages: list[dict] = [
            {"role": "user", "content": self._research_message(instructions, chapter_title, chapter_description)}
        ]
        tools = self._tools()

        # ---- Phase 1: research loop (tool use). Text here is reasoning, not the answer. ----
        for _ in range(_MAX_TOOL_ITERATIONS):
            _check_cancelled(self.run_id)

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=tools,
                messages=messages,
            )

            turn_text = "".join(b.text for b in response.content if b.type == "text")
            if turn_text.strip():
                await self.bus.publish(
                    self.run_id,
                    {"type": "agent_message", "data": {"role": "agent", "content": turn_text, "message_type": "thought"}},
                )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                break

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    await self.bus.publish(
                        self.run_id,
                        {"type": "agent_message", "data": {"role": "agent", "content": f"Using tool: {block.name} — {_describe_input(block.input)}", "message_type": "tool"}},
                    )
                    result_text = await self._run_tool(block.name, block.input, execute_tool)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_text,
                    })

            messages.append({"role": "user", "content": tool_results})

        # ---- Phase 2: finalize — dedicated, streamed, no tools → clean deliverable. ----
        _check_cancelled(self.run_id)
        final_instr = self._final_instruction(chapter_title)
        if messages and messages[-1]["role"] == "user":
            # Loop ended mid tool-cycle (hit max iterations): the last turn is a user
            # tool_results message. Append the instruction into it to keep roles alternating.
            content = messages[-1]["content"]
            if isinstance(content, list):
                content.append({"type": "text", "text": final_instr})
            else:
                messages[-1]["content"] = f"{content}\n\n{final_instr}"
        else:
            messages.append({"role": "user", "content": final_instr})

        final_text = ""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=messages,
        ) as stream:
            async for delta in stream.text_stream:
                final_text += delta
                await self.bus.publish(self.run_id, {"type": "streaming_chunk", "data": {"delta": delta}})

        return self._sanitize_final(final_text)

    def _sanitize_final(self, text: str) -> str:
        cleaned = _strip_code_fences(text.strip())
        if self.output_mode == "pptx":
            return _extract_json_object(cleaned)
        return cleaned

    async def _run_tool(self, name: str, inputs: dict, execute_tool) -> str:
        if name == "search_knowledge_base":
            chunks = KBStore.instance().search(self.report_id, inputs.get("query", ""), top_k=8)
            if not chunks:
                return "No relevant excerpts found in the knowledge base."
            return "\n\n---\n\n".join(f"[{c['filename']}]\n{c['text']}" for c in chunks)
        return await execute_tool(name, inputs)


def _describe_input(inputs: dict) -> str:
    if "query" in inputs:
        return str(inputs["query"])
    if "url" in inputs:
        return str(inputs["url"])
    return json.dumps(inputs)


def _strip_code_fences(text: str) -> str:
    """Remove a wrapping ```lang ... ``` fence if the whole message is fenced."""
    t = text.strip()
    m = re.match(r"^```[a-zA-Z0-9]*\s*\n(.*?)\n?```$", t, re.DOTALL)
    if m:
        return m.group(1).strip()
    return t


def _extract_json_object(text: str) -> str:
    """Pull the slide JSON object out of the text even if the model added a preamble or
    wrapped it in ```json fences."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass
    return text
