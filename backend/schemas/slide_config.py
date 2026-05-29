from datetime import datetime

from pydantic import BaseModel


class SlideConfigUpsert(BaseModel):
    output_mode: str = "markdown"
    slide_ratio: str = "16:9"
    title_font: str = "Calibri"
    title_font_size: int = 36
    title_bold: bool = True
    title_color: str = "1F2937"
    body_font: str = "Calibri"
    body_font_size: int = 20
    body_bold: bool = False
    body_color: str = "374151"
    bg_color: str = "FFFFFF"
    margin_top: float = 0.7
    margin_left: float = 0.7
    margin_right: float = 0.7
    margin_bottom: float = 0.7


class SlideConfigOut(SlideConfigUpsert):
    id: int
    chapter_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
