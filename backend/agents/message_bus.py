from __future__ import annotations

import asyncio
from collections import defaultdict


class MessageBus:
    _instance: MessageBus | None = None

    def __init__(self) -> None:
        self._subscribers: dict[int, list[asyncio.Queue]] = defaultdict(list)

    @classmethod
    def instance(cls) -> MessageBus:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def subscribe(self, run_id: int) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._subscribers[run_id].append(q)
        return q

    async def publish(self, run_id: int, event: dict) -> None:
        for q in self._subscribers.get(run_id, []):
            await q.put(event)

    def unsubscribe(self, run_id: int, queue: asyncio.Queue) -> None:
        subs = self._subscribers.get(run_id, [])
        if queue in subs:
            subs.remove(queue)
