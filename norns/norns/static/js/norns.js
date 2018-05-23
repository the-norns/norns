let CANVAS_WIDTH = 1000;
let CANVAS_HEIGHT = 470;
let tileX = 50;
let tileY = 50;
const FPS = 60;

let canvasElement = $("<canvas width='" + CANVAS_WIDTH + 
                      "' height='" + CANVAS_HEIGHT + "'></canvas>");
let canvas = canvasElement.get(0).getContext("2d");
canvasElement.appendTo($(".game"));

setInterval(function() {
  update();
  draw();
}, 1000/FPS);

function update() {
  tileX += 1;
  tileY += 1;
}

function draw() {
  canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  canvas.fillStyle = "#000";
  canvas.fillText("Hello World", tileX, tileY);
}