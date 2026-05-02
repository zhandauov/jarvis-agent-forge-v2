from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from agents.message_bus import MessageBus

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/runs/{run_id}")
async def ws_run(websocket: WebSocket, run_id: int):
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
