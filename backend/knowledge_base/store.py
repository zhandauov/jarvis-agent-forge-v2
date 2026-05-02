from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class ChunkEntry:
    doc_id: int
    filename: str
    chunk_index: int
    text: str


class KBStore:
    _instance: KBStore | None = None

    def __init__(self) -> None:
        self._index: dict[int, list[ChunkEntry]] = defaultdict(list)

    @classmethod
    def instance(cls) -> KBStore:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_document(self, report_id: int, doc_id: int, filename: str, chunks: list[str]) -> None:
        self.remove_document(report_id, doc_id)
        for i, text in enumerate(chunks):
            self._index[report_id].append(ChunkEntry(doc_id=doc_id, filename=filename, chunk_index=i, text=text))

    def remove_document(self, report_id: int, doc_id: int) -> None:
        self._index[report_id] = [e for e in self._index[report_id] if e.doc_id != doc_id]

    def search(self, report_id: int, query: str, top_k: int = 10) -> list[dict]:
        tokens = set(re.findall(r"\w+", query.lower()))
        if not tokens:
            return []

        entries = self._index.get(report_id, [])
        scored: list[tuple[float, ChunkEntry]] = []
        for entry in entries:
            entry_tokens = set(re.findall(r"\w+", entry.text.lower()))
            overlap = len(tokens & entry_tokens)
            if overlap > 0:
                score = overlap / (len(tokens) + 0.1)
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"doc_id": e.doc_id, "filename": e.filename, "chunk_index": e.chunk_index, "text": e.text}
            for _, e in scored[:top_k]
        ]

    async def reload_from_db(self) -> None:
        from sqlalchemy import select
        from core.database import AsyncSessionLocal
        from models.knowledge_base import KBDocument
        from knowledge_base.extractor import load_chunks

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(KBDocument).where(KBDocument.status == "ready"))
            docs = result.scalars().all()
            for doc in docs:
                chunks = load_chunks(doc.file_path)
                if chunks:
                    self.add_document(doc.report_id, doc.id, doc.filename, chunks)
