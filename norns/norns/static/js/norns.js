let CANVAS_WIDTH = 1000;
let CANVAS_HEIGHT = 470;
let tileX = 50;
let tileY = 50;
const FPS = 60;
const __API_URL__ = 'http://localhost:8000/api/v1/'
// var tileRender = {
//   color: "#00A",
//   x: 0,
//   y: 0,
//   width: 32,
//   height: 32,
//   draw: function() {
//     canvas.fillStyle = this.color;
//     canvas.fillRect(this.x, this.y, this.width, this.height);
//   }
// };

function Tile(x, y) {
    this.x = x;
    this.y = y;
    this.width = 32;
    this.height = 32;
    this.color = "#00A";
    this.draw = function() {
    canvas.fillStyle = this.color;
    canvas.fillRect(this.x, this.y, this.width, this.height);
  }
}

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

$.post(`${__API_URL__}room/new`, function (data) {
    // console.log(data)
    data.tiles.forEach(function(tile){
        testTile = new Tile(tile.x_coord, tile.y_coord, "#00A")
        console.log(testTile)
        testTile.draw()
    })
})