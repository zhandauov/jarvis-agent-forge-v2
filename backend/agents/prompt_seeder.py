from agents.prompts import (
    AGGREGATE_USER_TEMPLATE,
    KB_SECTION_TEMPLATE,
    PLAN_USER_TEMPLATE,
    PPTX_AGGREGATE_USER_TEMPLATE,
    REVIEW_USER_TEMPLATE,
    SUPERVISOR_SYSTEM_DEFAULT,
    WORKER_SYSTEM_DEFAULT,
)

PROMPT_DEFAULTS = [
    {
        "key": "supervisor_system",
        "name": "Supervisor System Prompt",
        "description": "System prompt for the supervisor agent. No template variables — sets the agent's persona and behavior.",
        "body": SUPERVISOR_SYSTEM_DEFAULT,
    },
    {
        "key": "worker_system",
        "name": "Worker System Prompt",
        "description": "System prompt for each worker agent. No template variables — sets the worker's persona and behavior.",
        "body": WORKER_SYSTEM_DEFAULT,
    },
    {
        "key": "plan_user",
        "name": "Planning Prompt",
        "description": "User message that asks the supervisor to create a research plan. Variables: {chapter_title}, {chapter_description}, {kb_section}, {worker_roles_list}",
        "body": PLAN_USER_TEMPLATE,
    },
    {
        "key": "review_user",
        "name": "Review Prompt",
        "description": "User message that asks the supervisor to review worker findings and decide if more research is needed. Variables: {chapter_title}, {worker_outputs}",
        "body": REVIEW_USER_TEMPLATE,
    },
    {
        "key": "aggregate_user",
        "name": "Aggregation Prompt",
        "description": "User message that asks the supervisor to write the final chapter section. Variables: {chapter_title}, {chapter_description}, {all_findings}, {kb_section}",
        "body": AGGREGATE_USER_TEMPLATE,
    },
    {
        "key": "kb_section",
        "name": "Knowledge Base Section Template",
        "description": "Template used to format knowledge base chunks into agent context. Variables: {chunks}",
        "body": KB_SECTION_TEMPLATE,
    },
    {
        "key": "pptx_aggregate_user",
        "name": "Slide Aggregation Prompt (PPTX)",
        "description": "Used instead of the normal aggregation prompt when output mode is PPTX. Instructs the supervisor to return JSON with title + bullets for a single slide. Variables: {chapter_title}, {chapter_description}, {all_findings}, {kb_section}",
        "body": PPTX_AGGREGATE_USER_TEMPLATE,
    },
]


async def seed_default_prompts() -> None:
    from core.database import AsyncSessionLocal
    from models.prompt_template import PromptTemplate
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        for defaults in PROMPT_DEFAULTS:
            result = await db.execute(
                select(PromptTemplate).where(PromptTemplate.key == defaults["key"])
            )
            if result.scalar_one_or_none() is None:
                db.add(PromptTemplate(**defaults))
        await db.commit()
