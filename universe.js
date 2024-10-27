import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
// renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.25;

const ellipseCurve = new THREE.EllipseCurve(
    0, 0,            // ax, aY
    30, 20,          // xRadius, yRadius
    0, 2 * Math.PI,  // aStartAngle, aEndAngle
    false,           // aClockwise
    0                // aRotation
);

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5).normalize();
light.castShadow = true;
light.shadow.bias = -0.0001;
scene.add(light);

const sphereGeometry = new THREE.SphereGeometry(0.2, 32, 32);
const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, emissive: 0xffffff });
const lightSphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
scene.add(lightSphere);

// const toplight = new THREE.DirectionalLight(0xffffff, 0.2);
// toplight.position.set(-50, 100, -50).normalize();
// toplight.castShadow = true;
// scene.add(toplight);

// const botlight = new THREE.DirectionalLight(0xffffff, 0.2);
// botlight.position.set(-50, -100, -50).normalize();
// botlight.castShadow = true;
// scene.add(botlight);

// Cube
// const cubeGeometry = new THREE.BoxGeometry();
// const cubeMaterial = new THREE.MeshStandardMaterial({ color: 0x0077ff });
// const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
// cube.castShadow = true;
// cube.receiveShadow = true;
// scene.add(cube);

// Torus
const textureLoader = new THREE.TextureLoader();
let torus = null;
const img = new Image();
img.src = 'Earth_map.jpg';
img.onload = function() {
    const { img_top, img_bottom } = cutImageInHalves(img);
    const torusTexture = glueImgHalves(img_top, img_bottom);
    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(torusTexture, function(torusTexture) {
        const geometry = new THREE.TorusGeometry(10, 3, 16, 100);
        const material = new THREE.MeshStandardMaterial({ map: torusTexture, side: THREE.DoubleSide });
        torus = new THREE.Mesh(geometry, material);
        torus.castShadow = false;
        torus.receiveShadow = false;
        torus.rotation.x = -Math.PI / 2;
        scene.add(torus);
    });
};

const axesHelper = new THREE.AxesHelper( 5 );
scene.add( axesHelper );

// const texture = textureLoader.load('Earth_map.jpg');

// const torusGeometry = new THREE.TorusGeometry(10, 3, 16, 100);
// torusGeometry.center = (0.5, 0);
// const material = new THREE.MeshStandardMaterial({ map: texture});
// const torus = new THREE.Mesh(torusGeometry, material);
// torus.castShadow = false;
// torus.receiveShadow = false;
// scene.add(torus);

let time = 0;
const speed = 0.001; // Adjust the speed of the orbit
const torusRotationSpeed = 0.0001;
let torusCurrentAngle = 0;

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Update controls
    controls.update();

    // Calculate the position on the ellipse
    const point = ellipseCurve.getPoint(time);
    light.position.set(point.x, point.y, 0);
    lightSphere.position.copy(light.position);
    if(torus) {
        torusCurrentAngle += torusRotationSpeed;
        torus.rotation.z = (Math.PI * torusCurrentAngle);
        if(torusCurrentAngle >= 2) {
            torusCurrentAngle = 0;
        }
    }

    // Increment time to move along the curve
    time += speed;
    if (time > 1) {
        time = 0; // Loop the animation
    }

    // Render scene
    renderer.render(scene, camera);
}

// Initial camera position
camera.position.set(10, 10, 30);
controls.update();

animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

function cutImageInHalves(img) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const width = img.width;
    const height = img.height;
    const halfHeight = Math.floor(height / 2);
    
    canvas.width = width;
    canvas.height = height;
    
    // Draw the image on the canvas
    ctx.drawImage(img, 0, 0);
    
    // Get the top half
    const img_top = ctx.getImageData(0, 0, width, halfHeight);
    
    // Get the bottom half
    const img_bottom = ctx.getImageData(0, halfHeight, width, halfHeight);
    
    return { img_top, img_bottom };
}

function glueImgHalves(img_top, img_bottom) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const width = img_top.width;
    const height = img_top.height + img_bottom.height;
    
    canvas.width = width;
    canvas.height = height;
    
    // Draw the bottom half on the top
    ctx.putImageData(img_bottom, 0, 0);
    
    // Draw the top half on the bottom
    ctx.putImageData(img_top, 0, img_bottom.height);
    
    // Convert the canvas to a data URL
    return canvas.toDataURL();
}


// const scene = new THREE.Scene();
// const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// const renderer = new THREE.WebGLRenderer();
// renderer.setSize(window.innerWidth, window.innerHeight);
// document.body.appendChild(renderer.domElement);

// camera.position.z = 50;

// function animate() {
// requestAnimationFrame(animate);
// torus.rotation.x += 0.01;
// torus.rotation.y += 0.01;
// renderer.render(scene, camera);
// }
// animate();

/////////////////////////////////////////////////
// const textureLoader = new THREE.TextureLoader();
// const texture = textureLoader.load('path/to/your/image.jpg');

// const geometry = new THREE.TorusGeometry(10, 3, 16, 100);
// const material = new THREE.MeshBasicMaterial({ map: texture });
// const torus = new THREE.Mesh(geometry, material);
// scene.add(torus);

// const scene = new THREE.Scene();
// const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// const renderer = new THREE.WebGLRenderer();
// renderer.setSize(window.innerWidth, window.innerHeight);
// document.body.appendChild(renderer.domElement);

// camera.position.z = 50;

// function animate() {
// requestAnimationFrame(animate);
// torus.rotation.x += 0.01;
// torus.rotation.y += 0.01;
// renderer.render(scene, camera);
// }
// animate();

////////////////////////////////////////////////////

// const scene = new THREE.Scene();
// const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// const renderer = new THREE.WebGLRenderer();
// renderer.setSize(window.innerWidth, window.innerHeight);
// document.body.appendChild(renderer.domElement);

// const textureLoader = new THREE.TextureLoader();
// const texture = textureLoader.load('path/to/your/image.jpg');

// const geometry = new THREE.TorusGeometry(10, 3, 16, 100);
// const material = new THREE.MeshBasicMaterial({ map: texture });
// const torus = new THREE.Mesh(geometry, material);
// scene.add(torus);

// camera.position.z = 50;

// const renderTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);

// renderer.setRenderTarget(renderTarget);
// renderer.render(scene, camera);
// renderer.setRenderTarget(null);

// const pixelBuffer = new Uint8Array(window.innerWidth * window.innerHeight * 4);
// renderer.readRenderTargetPixels(renderTarget, 0, 0, window.innerWidth, window.innerHeight, pixelBuffer);

// const canvas = document.createElement('canvas');
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;
// const context = canvas.getContext('2d');
// const imageData = context.createImageData(window.innerWidth, window.innerHeight);
// imageData.data.set(pixelBuffer);
// context.putImageData(imageData, 0, 0);
// const dataURL = canvas.toDataURL();

// const socket = new WebSocket('ws://your-websocket-server');
// socket.onopen = () => {
// socket.send(dataURL);
// };