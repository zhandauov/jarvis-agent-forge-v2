import json
import re
from io import BytesIO

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


def _hex_to_rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#").strip()
    if len(h) != 6:
        h = "000000"
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return RGBColor(r, g, b)


def parse_slide_content(raw: str) -> tuple[str, list[str]]:
    stripped = raw.strip()
    stripped = re.sub(r"^```json\s*", "", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"```\s*$", "", stripped)
    stripped = stripped.strip()
    try:
        data = json.loads(stripped)
        title = str(data.get("title", ""))
        bullets = data.get("bullets", [])
        if isinstance(bullets, list):
            return title, [str(b) for b in bullets]
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
    lines = [l.strip() for l in stripped.splitlines() if l.strip()]
    title = lines[0].lstrip("#").strip() if lines else ""
    bullets = [l.lstrip("-•* ").strip() for l in lines[1:] if l.strip()]
    return title, bullets


def _add_text_run(paragraph, text: str, font_name: str, font_size: int, bold: bool, color_hex: str) -> None:
    run = paragraph.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = _hex_to_rgb(color_hex)


def build_slide(raw_content: str, slide_config, chapter_title: str) -> bytes:
    title_text, bullets = parse_slide_content(raw_content)
    if not title_text:
        title_text = chapter_title

    prs = Presentation()

    if slide_config.slide_ratio == "4:3":
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
    else:
        prs.slide_width = Inches(13.33)
        prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = _hex_to_rgb(slide_config.bg_color)

    w = prs.slide_width
    h = prs.slide_height
    ml = Inches(slide_config.margin_left)
    mt = Inches(slide_config.margin_top)
    mr = Inches(slide_config.margin_right)
    mb = Inches(slide_config.margin_bottom)
    content_w = w - ml - mr

    # Title box
    title_h = Inches(1.4)
    title_box = slide.shapes.add_textbox(ml, mt, content_w, title_h)
    title_box.text_frame.word_wrap = True
    title_para = title_box.text_frame.paragraphs[0]
    _add_text_run(title_para, title_text,
                  slide_config.title_font, slide_config.title_font_size,
                  slide_config.title_bold, slide_config.title_color)

    # Body box
    body_top = mt + title_h + Inches(0.15)
    body_h = h - body_top - mb
    body_box = slide.shapes.add_textbox(ml, body_top, content_w, body_h)
    body_box.text_frame.word_wrap = True

    for i, bullet in enumerate(bullets):
        para = body_box.text_frame.paragraphs[0] if i == 0 else body_box.text_frame.add_paragraph()
        _add_text_run(para, f"•  {bullet}",
                      slide_config.body_font, slide_config.body_font_size,
                      slide_config.body_bold, slide_config.body_color)

    buf = BytesIO()
    prs.save(buf)
    return buf.getvalue()
