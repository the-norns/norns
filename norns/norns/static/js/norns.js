let CANVAS_WIDTH = 600;
let CANVAS_HEIGHT = 470;
let roomTiles = [];
const __API_URL__ = 'http://localhost:8000/api/v1/'

let canvasElement = $("<canvas width='" + CANVAS_WIDTH + 
                      "' height='" + CANVAS_HEIGHT + "'></canvas>");
let canvas = canvasElement.get(0).getContext("2d");

canvasElement.appendTo($(".game"));

function Tile(x, y, consumables, enemies, players, weapons) {
    this.x = x;
    this.y = y;
    this.color = "#00A";
    this.enemies = enemies;
    this.players = players;
    this.weapons = weapons;
    this.draw = function() {
    canvas.fillStyle = this.color;
    canvas.fillRect(this.x * 100, this.y * 100, 99, 99);
  }
}

function draw(tiles) {
  tiles.forEach(function(tile){tile.draw()})
}

function newGame() {
    $(".start-game").remove()
    $.post(`${__API_URL__}room/new`, function (data) {
    data.tiles.forEach(function(tile){
        roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
    })
  })
    .then(() => draw(roomTiles))
}

function clearCanvas() {
    canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
}

function action(event) {
    event.preventDefault()
    console.log(event.target.action.value)
    $.post(`${__API_URL__}room`, function(data){
        data.tiles.forEach(function(tile){
            roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
        })
    })
    .then(() => draw(roomTiles))
}

$(".start-game").on("click", newGame);
$(".action-form").on("submit", action);
