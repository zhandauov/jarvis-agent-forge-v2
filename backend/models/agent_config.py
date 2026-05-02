from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class AgentTeamConfig(Base):
    __tablename__ = "agent_team_configs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, unique=True)
    supervisor_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    worker_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    worker_roles: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array
    worker_count: Mapped[int] = mapped_column(Integer, default=3)
    max_rounds: Mapped[int] = mapped_column(Integer, default=4)
    model: Mapped[str] = mapped_column(String(100), default="claude-opus-4-7")
    internet_access: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="agent_config")
