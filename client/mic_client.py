import sounddevice as sd
import websockets
import asyncio
import numpy as np
import json
import time

class AudioClient:
    def __init__(self):
        self.sample_rate = 16000
        self.chunk_size = 480 
        self.stream = None
        self.websocket = None
        self.loop = None
        self.running = True
        self.last_sent = time.time()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(
                "ws://localhost:8765",
                ping_interval=20,
                ping_timeout=60
            )
            print("Connected to server")
            
            self.stream = sd.InputStream(
                callback=self.audio_callback,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                channels=1
            )
            
        except Exception as e:
            print(f"error: {e}")
            raise

    def audio_callback(self, indata, frames, time_info, status):
        try:
            if status:
                print(f"Audio status: {status}")
                
            current_time = time.time()
            if current_time - self.last_sent > 1:
                print(f"Audio chunk: Max {np.max(indata):.2f}, Min {np.min(indata):.2f}")
                self.last_sent = current_time
                
            if self.websocket:
                audio = (indata * 32767).astype(np.int16)
                asyncio.run_coroutine_threadsafe(
                    self.send_audio(audio),
                    self.loop
                )
        except Exception as e:
            print(f"error: {e}")

    async def send_audio(self, audio_chunk):
        try:
            await self.websocket.send(audio_chunk.tobytes())
        except Exception as e:
            print(f"error: {e}")

    async def receive_responses(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                print(f"Response: {data['text']}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server")
        except Exception as e:
            print(f"Receive error: {e}")

    async def run(self):
        try:
            self.loop = asyncio.get_running_loop()
            await self.connect()
            with self.stream:
                print("Recording started...")
                await self.receive_responses()
        except Exception as e:
            print(f"Erorr: {e}")
        finally:
            self.running = False
            if self.websocket:
                await self.websocket.close()

if __name__ == "__main__":
    client = AudioClient()
    asyncio.run(client.run())







