import json
from typing import Dict
from fastapi import WebSocket
from app.core.logger import logger

class ConnectionManager:
    """
    Stateful registry tracking active WebSocket client sessions.
    Maps User IDs -> active WebSockets, enabling targeted and broadcast alerts.
    """
    def __init__(self):
        # Active sessions maps: user_id (string) -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        Accepts a WebSocket connection and registers the user ID.
        """
        await websocket.accept()
        # Evict old connection if present to prevent leaks
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
            except Exception:
                pass
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket client connected: User ID '{user_id}'. Active channels: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        """
        Removes a disconnected user's socket from the active connection mapping.
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"WebSocket client disconnected: User ID '{user_id}'. Active channels: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, user_id: str) -> bool:
        """
        Transmits a JSON message directly to a user's active WebSocket channel.
        Returns True if successful, False if the user is offline.
        """
        websocket = self.active_connections.get(user_id)
        if not websocket:
            return False
            
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except Exception as e:
            logger.warning(f"Error transmitting to User ID '{user_id}', removing broken socket: {str(e)}")
            self.disconnect(user_id)
            return False

    async def broadcast(self, message: dict):
        """
        Sends a JSON message to all active WebSocket clients.
        """
        logger.info(f"Broadcasting websocket alert to {len(self.active_connections)} clients...")
        offline_users = []
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to broadcast to User ID '{user_id}': {str(e)}")
                offline_users.append(user_id)
                
        # Clean up stale connections
        for user_id in offline_users:
            self.disconnect(user_id)

manager = ConnectionManager()
