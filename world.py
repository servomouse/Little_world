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


def get_D(pov, screen, center, r):
    """ Discriminant
    pov, screen, center - coordinates like [x, y, z] """
    x0 = pov[0]
    x1 = screen[0]
    y0 = pov[1]
    y1 = screen[1]
    z0 = pov[2]
    z1 = screen[2]
    d = (y1 - y0) / (x1 - x0)
    e = (z1 - z0) / (x1 - x0)
    f = d * x0 + y0
    g = e * x0 + y0
    a = 1 + d**2 + e**2
    b = (-2 * d * f) - (2 * e * g)
    c = f**2 + g**2 - r**2
    D = b**2 - 4 * a * c
    return D


def get_Distance(pov, screen, center, r):
    """ Minimal distance
    pov, screen, center - coordinates like [x, y, z] """
    x0 = pov[0]
    x1 = screen[0]
    y0 = pov[1]
    y1 = screen[1]
    z0 = pov[2]
    z1 = screen[2]
    a = y1 - y0
    b = x1 - x0
    c = z1 - z0
    s = [b, a, c]
    M1 = [x0, y0, z0]   # Center of the sphere
    M0M1 = [x0, y0, z0]
    M0M1s = [M0M1[1] * s[2] - M0M1[2] * s[1], M0M1[0] * s[2] - M0M1[2] * s[0], M0M1[0] * s[1] - M0M1[1] * s[0]]
    D = sqrt(M0M1s[0]**2 + M0M1s[1]**2 + M0M1s[2]**2) / sqrt(s[0]**2 + s[1]**2 + s[2]**2)
    return D


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
                D = get_D(pov, [screen[0], y1, z1], [], r)
                if D < 0:
                    cells_data.append([y + h_width, z + h_height, dark_color])
                else:
                    cells_data.append([y + h_width, z + h_height, bright_color])

                if len(cells_data) > 250:
                    json_data = json.dumps(cells_data)
                    await websocket.send(json_data)
                    cells_data = []
                    await asyncio.sleep(0.1)


            # greeting = await websocket.recv()
            # print(f"Received data: {greeting}")
        await receive_task

asyncio.get_event_loop().run_until_complete(hello())
