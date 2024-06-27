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


connected_clients = set()

async def relay(websocket, path):
    if len(connected_clients) < 2:
        connected_clients.add(websocket)
        print(f"Connected client #{len(connected_clients)}")
        try:
            async for message in websocket:
                if len(connected_clients) == 2:
                    for client in connected_clients:
                        if client != websocket:
                            print(f"MYLOG: Resending data: {message}")
                            await client.send(message)
                else:
                    print(f"MYLOG: Data received, but there is no connection to resend: {len(connected_clients)}, {message}")
        finally:
            print("Removing client")
            connected_clients.remove(websocket)
    else:
        print(f"Illegal attempt to connect 3rd client")
        await websocket.close()


import_data('variables.js')
start_server = websockets.serve(relay, "localhost", ws_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()