"""Components for custom functionality."""

from typing import List
from fastapi import WebSocket


class Notifier:
    """
    A class for managing WebSocket connections and sending notifications to them.
    """
    
    def __init__(self):
        # List to store active WebSocket connections
        self.connections: List[WebSocket] = []
        # Start a notification generator coroutine
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        """
        A coroutine that waits for incoming messages and sends them to all connected WebSocket clients.
        """
        while True:
            # Wait for a new message to be sent to the generator
            message = yield
            # Send the message to all connected clients
            await self._notify(message)

    async def push(self, msg):
        """
        Pushes a notification message to the notification generator coroutine.
        """
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        """
        Adds a new WebSocket connection to the list of active connections.
        """
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the list of active connections.
        """
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        """
        Sends a notification message to all active WebSocket clients.
        """     
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        # Replace the old list of connections with the updated list
        self.connections = living_connections


# Create a new instance of the Notifier class
notifier = Notifier()
