const field_width = data.width;
const field_height = data.height;
const cell_size = 2;
const ws_port = data.port;
console.log(data.port);

const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');

canvas.width = field_width * cell_size;
canvas.height = field_height * cell_size;

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function setCellColor(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * cell_size, y * cell_size, cell_size, cell_size);
}

function red_random_cell() {
    x = getRandomInt(0, field_height);
    y = getRandomInt(0, field_width);
    setCellColor(x, y, '#F00');
}

function createWorld(height, width) {
    for (let row = 0; row < height; row++) {
        for (let col = 0; col < width; col++) {
            const color = (row + col) % 2 === 0 ? '#FFF' : '#000';
            setCellColor(col, row, color);
        }
    }
}

const ws = new WebSocket(`ws://localhost:${ws_port}`);

ws.onopen = function() {
    console.log('WebSocket connection established');
};

ws.onmessage = function(event) {
    console.log(`Received data ${event.data}`);
    const updates = JSON.parse(event.data);
    updates.forEach(([x, y, color]) => {setCellColor(x, y, color);});
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
};

console.log(`WebSocket server is running on ws://localhost:${ws_port}`);

createWorld(field_height, field_width);
setCellColor(0, 4, '#FF0000');
// setInterval(red_random_cell, 1000);

const toggles = document.querySelectorAll('input[type="radio"][name="toggle"]');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            if(this.checked) {
                // Send the name of the toggle to the WebSocket server
                console.log(`Toggle ${this.value} is enabled`);
                ws.send(`Toggle ${this.value} is enabled`);
        }
    });
});