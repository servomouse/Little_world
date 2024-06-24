# Little world

import websocket
import json
import random


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


if __name__ == "__main__":
    main()