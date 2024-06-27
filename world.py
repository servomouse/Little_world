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


def main():
    data = import_data('variables.js')

    # Accessing the variables
    port = data['port']
    width = data['width']
    height = data['height']
    w_center = int(width/2)
    h_center = int(height/2)

    def send_random_cells_to_websocket():
        ws = websocket.create_connection(f"ws://127.0.0.1:{port}")

        cells_data = []
        for _ in range(10):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            cells_data.append([x, y, color])

        json_data = json.dumps(cells_data)
        ws.send(json_data)
        ws.close()

    send_random_cells_to_websocket()


async def on_message(websocket):
    print("Message received: ", end='')
    async for message in websocket:
        print(f"{message}")


async def send_data(websocket, data):
    await websocket.send(data)
    # print(f"Data sent {data}")


async def main_logic():
    data = import_data('variables.js')

    # Accessing the variables
    port = data['port']
    width = data['width']
    height = data['height']
    w_center = int(width/2)
    h_center = int(height/2)
    uri = f"ws://127.0.0.1:{port}"
    async with websockets.connect(uri) as websocket:
        receive_task = asyncio.create_task(on_message(websocket))
    print(f"MYLOG: Connected to {uri}")
    # main logic
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
        # await send_data(websocket, json_data)
        time.sleep(10)

    await receive_task



if __name__ == "__main__":
    # main()
    asyncio.run(main_logic())