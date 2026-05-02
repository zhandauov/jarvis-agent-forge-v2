from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt

from agents.message_bus import MessageBus
from core.config import settings

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/runs/{run_id}")
async def ws_run(websocket: WebSocket, run_id: int, token: str = ""):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        if not payload.get("sub"):
            raise ValueError
    except (JWTError, ValueError):
        await websocket.close(code=1008)
        return

    await websocket.accept()
    bus = MessageBus.instance()
    queue = bus.subscribe(run_id)
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event)
            if event.get("type") in ("final_output", "error"):
                break
    except WebSocketDisconnect:
        pass
    finally:
        bus.unsubscribe(run_id, queue)
