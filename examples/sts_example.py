import asyncio
import json

import websockets
from fastapi import FastAPI, WebSocket

app = FastAPI()

OPENAI_API_KEY = "your-openai-api-key"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with websockets.connect(
        "wss://api.openai.com/v1/audio/speech",
        extra_headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
    ) as openai_ws:
        # Inicjalizacja sesji
        session_update = {
            "type": "session.update",
            "session": {
                "modalities": ["audio"],
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16"
            }
        }
        await openai_ws.send(json.dumps(session_update))

        async def receive_from_client():
            try:
                while True:
                    data = await websocket.receive_bytes()
                    await openai_ws.send(data)
            except Exception:
                pass

        async def send_to_client():
            try:
                while True:
                    data = await openai_ws.recv()
                    await websocket.send_bytes(data)
            except Exception:
                pass

        await asyncio.gather(receive_from_client(), send_to_client())
