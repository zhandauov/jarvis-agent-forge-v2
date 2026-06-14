from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Inline migration: add columns that may be missing in existing DBs
        for stmt in [
            "ALTER TABLE agent_team_configs ADD COLUMN internet_access BOOLEAN NOT NULL DEFAULT 0",
            "ALTER TABLE agent_team_configs ADD COLUMN aggregate_prompt TEXT",
            "ALTER TABLE agent_team_configs ADD COLUMN pptx_aggregate_prompt TEXT",
            "ALTER TABLE agent_team_configs ADD COLUMN mode VARCHAR(20) NOT NULL DEFAULT 'team'",
            "ALTER TABLE agent_team_configs ADD COLUMN single_agent_instructions TEXT",
        ]:
            try:
                await conn.execute(text(stmt))
            except Exception:
                pass  # column already exists
