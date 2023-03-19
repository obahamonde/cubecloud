from api import create_app
from api.config import env
from uvicorn import run
from starlette.types import ASGIApp, Receive, Scope, Send
from aiohttp import ClientSession
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse as RedirectResponse

app = create_app()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
</html>
"""

@app.get("/")
async def docs() -> RedirectResponse:
    return RedirectResponse(html)

import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from api.hooks.notify import Notifier
from api.data.schemas import WSMessage


notifier = Notifier()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await notifier.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await notifier.push(data)
    except WebSocketDisconnect:
        notifier.remove(ws)
        await notifier.generator.asend(None)


@app.on_event("startup")
async def startup_event():
    await notifier.generator.asend(None)
    
    
if __name__ == "__main__":
    run('main:app', host='0.0.0.0', port=80, reload=True)