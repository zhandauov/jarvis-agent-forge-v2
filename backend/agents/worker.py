import json
import re

import anthropic

from agents.models import WorkerResult

_MAX_TOOL_ITERATIONS = 10


class WorkerAgent:
    def __init__(
        self,
        role: str,
        worker_prompt: str,
        client: anthropic.AsyncAnthropic,
        model: str = "claude-sonnet-4-6",
        internet_access: bool = False,
    ) -> None:
        self.role = role
        self.system_prompt = worker_prompt
        self.client = client
        self.model = model
        self.internet_access = internet_access

    async def execute_task(self, task: str, kb_chunks: list[dict], bus=None, run_id: int | None = None) -> WorkerResult:
        kb_text = ""
        if kb_chunks:
            formatted = "\n\n---\n\n".join(f"[{c['filename']}]\n{c['text']}" for c in kb_chunks)
            kb_text = f"\n\nRelevant knowledge base excerpts:\n{formatted}"

        user_message = (
            f"Your role: {self.role}\n\n"
            f"Your task: {task}{kb_text}\n\n"
            f"Respond with JSON:\n"
            f'{{\"role\": \"{self.role}\", \"findings\": \"detailed findings\", \"data_points\": [\"key fact 1\", \"key fact 2\"]}}'
        )

        if self.internet_access:
            return await self._execute_with_tools(user_message, bus, run_id)
        return await self._execute_simple(user_message, bus, run_id)

    async def _execute_simple(self, user_message: str, bus=None, run_id: int | None = None) -> WorkerResult:
        if bus and run_id:
            full_text = ""
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=2048,
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_message}],
            ) as stream:
                async for delta in stream.text_stream:
                    full_text += delta
                    await bus.publish(run_id, {"type": "agent_streaming", "data": {"role": self.role, "delta": delta}})
            return self._parse_result(full_text)

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return self._parse_result(message.content[0].text)

    async def _execute_with_tools(self, user_message: str, bus=None, run_id: int | None = None) -> WorkerResult:
        from agents.tools import WEB_TOOLS, execute_tool

        messages: list[dict] = [{"role": "user", "content": user_message}]
        final_text = ""

        for _ in range(_MAX_TOOL_ITERATIONS):
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=WEB_TOOLS,
                messages=messages,
            )

            for block in response.content:
                if block.type == "text":
                    final_text = block.text

            if response.stop_reason == "end_turn":
                break

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        if bus and run_id:
                            await bus.publish(run_id, {"type": "agent_streaming", "data": {"role": self.role, "delta": f"*Using tool: {block.name}...*\n"}})
                        result_text = await execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text,
                        })

                messages.append({"role": "user", "content": tool_results})
            else:
                break

        return self._parse_result(final_text)

    def _parse_result(self, content: str) -> WorkerResult:
        try:
            data = json.loads(_extract_json(content))
            return WorkerResult(
                role=data.get("role", self.role),
                findings=data.get("findings", content),
                data_points=data.get("data_points", []),
            )
        except (json.JSONDecodeError, KeyError):
            return WorkerResult(role=self.role, findings=content)


def _extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text