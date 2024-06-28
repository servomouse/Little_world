# Little world

import websocket    # pip install websocket-client
import json
import random
import asyncio
import websockets
from math import sqrt
import time


def import_data(file_path):
    with open(file_path, 'r') as f:
        data_str = '\n'.join(f.read().split('\n')[1:-1])
        data = json.loads(data_str)
        return data


async def on_message(websocket):
    print("Message received: ", end='')
    async for message in websocket:
        print(f"{message}")


async def send_data(websocket, data):
    await websocket.send(data)
    # print(f"Data sent {data}")


async def hello():
    data = import_data('variables.js')

    port = data['port']
    width = data['width']
    height = data['height']
    w_center = int(width/2)
    h_center = int(height/2)
    uri = f"ws://127.0.0.1:{port}"
    async with websockets.connect(uri) as websocket:
        print(f"MYLOG: Connected to {uri}")
        distance = 100
        while True:
            cells_data = []
            for _ in range(10):
                x_min = 0 - distance
                x_max = distance
                x = random.randint(x_min, x_max)
                y_max = int(sqrt((distance * distance) - (x*x)))
                y_min = 0 - y_max
                y = random.randint(y_min, y_max)
                color = "#{:06x}".format(random.randint(0, 0x005500))
                cells_data.append([w_center+x, h_center+y, color])

            json_data = json.dumps(cells_data)
            await websocket.send(json_data)
            await asyncio.sleep(0.1)

            # greeting = await websocket.recv()
            # print(f"Received data: {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
