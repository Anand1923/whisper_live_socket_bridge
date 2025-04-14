import asyncio
import websockets
import json
import uuid
import logging

WHISPER_URI = "ws://localhost:9090/client"
BRIDGE_SERVER_HOST = "localhost"
BRIDGE_SERVER_PORT = 8765

async def send_to_whisper(audio_queue):
    try:
        uid = str(uuid.uuid4())
        async with websockets.connect(WHISPER_URI, ping_interval=None) as whisper_ws:
            print("Connected to Whisper")

            await whisper_ws.send(json.dumps({
                "event": "start",
                "uid": uid,
                "model": "tiny",
                "sample_rate": 16000,
                "language": "en",
                "task": "transcribe"
            }))

            while True:
                audio_data = await audio_queue.get()
                if audio_data is None:
                    break  
                await whisper_ws.send(audio_data)


            await whisper_ws.send(json.dumps({
                "event": "end",
                "uid": uid,
                "model": "tiny",
                "sample_rate": 16000,
                "language": "en",
                "task": "transcribe"
            }))

            while True:
                try:
                    result = await asyncio.wait_for(whisper_ws.recv(), timeout=10.0)
                    print(f"transcription: {result}")
                except asyncio.TimeoutError:
                    print("Whisper timeout")
                    break

    except Exception as e:
        print(f"Error:{e}")


async def handle_client(websocket):
    print("Client connected")
    audio_queue = asyncio.Queue()

    whisper_task = asyncio.create_task(send_to_whisper(audio_queue))

    try:
        async for message in websocket:
            await audio_queue.put(message)


    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        await audio_queue.put(None)
        await whisper_task
        print("Final")

async def main():
    logging.basicConfig(level=print)
    async with websockets.serve(handle_client, BRIDGE_SERVER_HOST, BRIDGE_SERVER_PORT):
        print(f"Bridge server running at ws://{BRIDGE_SERVER_HOST}:{BRIDGE_SERVER_PORT}")
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
















