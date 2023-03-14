import json
from typing import Dict, List, Optional, Union
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.router.github import get_tree_recursive
from api.utils.gen import gen_oid, gen_now
from api.utils.get import get_base64
from api.utils.fmt import *
from api.utils.misc import *
from api.schemas.components import Notifier

class WSNotifier(APIRouter):
    def __init__(self):
        super().__init__(prefix="/ws", tags=["ws"])
        self.notifiers: Dict[str, Notifier] = {}
        self.connections: Dict[str, WebSocket] = {}
        self.tree: Dict[str, Dict[str, str]] = {}
        
    @property
    def notifier(self)->Notifier:
        return self.notifiers.get("notifier", Notifier())

    async def connect(self, sub: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[sub] = websocket
        await self.notifier.connect(websocket)

    def remove(self, sub: str, websocket: WebSocket):
        self.connections.pop(sub)
        self.notifier.remove(websocket)
        
    async def push(self, sub: str, msg: str):
        await self.notifier.push(json.dumps({"sub": sub, **json.loads(msg)}))
        
        
app = WSNotifier()

@app.websocket("/{sub}")
async def websocket_endpoint(sub: str, websocket: WebSocket):
    await app.connect(sub, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await app.push(sub, data)
    except WebSocketDisconnect:
        app.remove(sub, websocket)
    