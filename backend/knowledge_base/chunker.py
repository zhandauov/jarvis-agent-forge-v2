import re


def chunk_text(text: str, min_size: int = 200, max_size: int = 800) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks: list[str] = []
    buffer = ""

    for para in paragraphs:
        if len(para) > max_size:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for sentence in sentences:
                if len(buffer) + len(sentence) <= max_size:
                    buffer = (buffer + " " + sentence).strip()
                else:
                    if buffer:
                        chunks.append(buffer)
                    buffer = sentence[:max_size]
        else:
            if len(buffer) + len(para) + 2 <= max_size:
                buffer = (buffer + "\n\n" + para).strip() if buffer else para
            else:
                if len(buffer) >= min_size:
                    chunks.append(buffer)
                elif chunks:
                    chunks[-1] = (chunks[-1] + "\n\n" + buffer).strip()
                buffer = para

    if buffer:
        if chunks and len(buffer) < min_size:
            chunks[-1] = (chunks[-1] + "\n\n" + buffer).strip()
        else:
            chunks.append(buffer)

    return [c for c in chunks if c]
