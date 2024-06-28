import asyncio
import websockets
import json

ws_port = 8765 # default value


def import_data(file_path):
    global ws_port
    with open(file_path, 'r') as f:
        data_str = '\n'.join(f.read().split('\n')[1:-1])
        data = json.loads(data_str)
        ws_port = data["port"]


connected = set()

async def relay(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        # Wait for exactly two clients to connect.
        while len(connected) < 2:
            await asyncio.sleep(0.1)  # Sleep briefly to avoid busy waiting.

        # Relay messages between the two clients.
        while True:
            message = await websocket.recv()
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("A client just disconnected")
    finally:
        # Unregister.
        print("A client just unregistered")
        connected.remove(websocket)


async def main():
    async with websockets.serve(relay, "localhost", ws_port):
        print(f"Server started on ws://localhost:{ws_port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())