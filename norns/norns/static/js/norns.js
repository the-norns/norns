let CANVAS_WIDTH = 1000;
let CANVAS_HEIGHT = 470;
let roomTiles = [];
const __API_URL__ = 'http://localhost:8000/api/v1/'

let canvasElement = $("<canvas width='" + CANVAS_WIDTH + 
                      "' height='" + CANVAS_HEIGHT + "'></canvas>");
let canvas = canvasElement.get(0).getContext("2d");

canvasElement.appendTo($(".game"));

function Tile(x, y, color) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.draw = function() {
    canvas.fillStyle = this.color;
    canvas.fillRect(this.x * 10, this.y * 10, 5, 5);
  }
}

$.post(`${__API_URL__}room/new`, function (data) {
    data.tiles.forEach(function(tile){
        roomTiles.push(new Tile(tile.x_coord, tile.y_coord, "#00A"))
    })
})
.then(console.log(roomTiles))
.then(() => draw(roomTiles))


function draw(tiles) {
  // canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  tiles.forEach(function(tile){tile.draw()})
}
