from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.connection_manager import manager
from app.core.logger import logger

router = APIRouter(prefix="/ws", tags=["Real-time WebSockets"])

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    Stateful WebSocket endpoint mapping active connections to User IDs.
    """
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Maintain connection, listen for keep-alive frames or client requests
            data = await websocket.receive_text()
            # Respond to ping frames to avoid network idle timeouts
            if data == "ping":
                await websocket.send_text("pong")
            else:
                logger.info(f"Received WebSocket data frame from User ID '{user_id}': {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket execution error on User ID '{user_id}': {str(e)}")
        manager.disconnect(user_id)
