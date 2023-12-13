// <!-- <!DOCTYPE html>
// <html lang="en">

// <head>
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/simplex-noise/2.4.0/simplex-noise.min.js"></script>
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.9/dat.gui.min.js"></script>
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/paper.js/0.12.17/paper-full.min.js"
//         integrity="sha512-NApOOz1j2Dz1PKsIvg1hrXLzDFd62+J0qOPIhm8wueAnk4fQdSclq6XvfzvejDs6zibSoDC+ipl1dC66m+EoSQ=="
//         crossorigin="anonymous" referrerpolicy="no-referrer"></script>
//     <meta charset="utf-8" />
// </head>

// <body>
//     <script src="other.js"></script>
//     <script src="poly.js"></script>
//     <script src="sketch.js"></script>
// </body>

// </html> -->

// TODO

const urlParams = new URLSearchParams(window.location.search);
let hash = urlParams.get('hash') ?? ''
let file = urlParams.get('file') ?? ''
var gui = new dat.gui.GUI();
gui.domElement.style.transform = 'scale(2, 2)' + 'translate(-25%, 25%)';

let P = {}

function setupParams() {
    permanentParams()
    P.file = file
}


function setup() {
    createCanvas(windowWidth, windowHeight)
    pixelDensity(2)
    setupParams()
    setupRandom()

}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    W = width
    H = height
    redraw()
}

function draw() {
    stroke(0)
    fill(0)
    textSize(30)
    text('file: ' + file, W / 8, H / 2)
}


function saveNamed(name = '') {
    let time = new Date().toISOString().slice(0, 19).replace(/:/g, "-");
    name = `vis-${file}-${time}`
    saveCanvas(name, 'png')
}
