from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class SlideConfig(Base):
    __tablename__ = "slide_configs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, unique=True)

    output_mode: Mapped[str] = mapped_column(String(20), default="markdown", server_default="markdown")
    slide_ratio: Mapped[str] = mapped_column(String(10), default="16:9", server_default="16:9")

    title_font: Mapped[str] = mapped_column(String(100), default="Calibri", server_default="Calibri")
    title_font_size: Mapped[int] = mapped_column(Integer, default=36, server_default="36")
    title_bold: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    title_color: Mapped[str] = mapped_column(String(6), default="1F2937", server_default="1F2937")

    body_font: Mapped[str] = mapped_column(String(100), default="Calibri", server_default="Calibri")
    body_font_size: Mapped[int] = mapped_column(Integer, default=20, server_default="20")
    body_bold: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    body_color: Mapped[str] = mapped_column(String(6), default="374151", server_default="374151")

    bg_color: Mapped[str] = mapped_column(String(6), default="FFFFFF", server_default="FFFFFF")

    margin_top: Mapped[float] = mapped_column(Float, default=0.7, server_default="0.7")
    margin_left: Mapped[float] = mapped_column(Float, default=0.7, server_default="0.7")
    margin_right: Mapped[float] = mapped_column(Float, default=0.7, server_default="0.7")
    margin_bottom: Mapped[float] = mapped_column(Float, default=0.7, server_default="0.7")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="slide_config")
