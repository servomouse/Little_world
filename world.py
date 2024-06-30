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
    async for message in websocket:
        print(f"Message received: {message}")


async def send_data(websocket, data):
    await websocket.send(data)
    # print(f"Data sent {data}")


# point of view = [x, y, z]
# screen position = [x, y, z]
def get_data(pov, screen):
    cell_size = 0.004
    h_width = 125
    h_height = 125
    bright_color = 0x005500
    dark_color = 0x002200
    cells_data = []
    r = 1
    for z1 in range(-h_height, h_height, cell_size):
        for y1 in range(-h_width, h_width, cell_size):
            x0 = pov[0]
            x1 = screen[0]
            y0 = pov[1]
            z0 = pov[2]
            a = y1 - y0
            b = x1 - x0
            c = z1 - z0
            f = a/b
            g = c/b
            d = (f*x0) + y0
            e = (g*x0) + z0
            D = (2*d*f - 2*e*g)**2 - 4 * (1 + f**2 + g**2) * (d**2 + e**2 + r**2)
            if D >= 0:
                cells_data.append(y1 + h_width, z1 + h_height, bright_color)
            else:
                cells_data.append(y1 + h_width, z1 + h_height, dark_color)


async def hello():
    data = import_data('variables.js')

    port = data['port']
    width = data['width']
    height = data['height']
    w_center = int(width/2)
    h_center = int(height/2)
    uri = f"ws://127.0.0.1:{port}"
    async with websockets.connect(uri) as websocket:
        receive_task = asyncio.create_task(on_message(websocket))
        print(f"MYLOG: Connected to {uri}")
        pov = [3, 0, 0]
        screen = [2, 0, 0]

        cell_size = 0.004
        h_width = 125
        h_height = 125
        bright_color = "#{:06x}".format(0x005500)
        dark_color = "#{:06x}".format(0x002200)
        cells_data = []
        r = 1
        for z in range(-h_height, h_height, 1):
            z1 = z * cell_size
            for y in range(-h_width, h_width, 1):
                y1 = y * cell_size
                x0 = pov[0]
                x1 = screen[0]
                y0 = pov[1]
                z0 = pov[2]
                a = y1 - y0
                b = x1 - x0
                c = z1 - z0
                f = a/b
                g = c/b
                d = (f*x0) + y0
                e = (g*x0) + z0
                D = (2*d*f - 2*e*g)**2 - 4 * (1 + f**2 + g**2) * (d**2 + e**2 - r**2)
                if D >= 0:
                    cells_data.append([y + h_width, z + h_height, bright_color])
                else:
                    cells_data.append([y + h_width, z + h_height, dark_color])

                if len(cells_data) > 250:
                    json_data = json.dumps(cells_data)
                    await websocket.send(json_data)
                    cells_data = []
                    await asyncio.sleep(0.1)


            # greeting = await websocket.recv()
            # print(f"Received data: {greeting}")
        await receive_task

asyncio.get_event_loop().run_until_complete(hello())
