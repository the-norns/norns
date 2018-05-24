let CANVAS_WIDTH = 600;
let CANVAS_HEIGHT = 470;
let roomTiles = [];
const __API_URL__ = 'http://localhost:8000/api/v1/'

let canvasElement = $("<canvas width='" + CANVAS_WIDTH + 
                      "' height='" + CANVAS_HEIGHT + "'></canvas>");
let canvas = canvasElement.get(0).getContext("2d");

canvasElement.appendTo($(".game"));

function destroyCanvas () { 
  let canvasElement = $("<canvas width='" + CANVAS_WIDTH + 
                      "' height='" + CANVAS_HEIGHT + "'></canvas>");
  let canvas = canvasElement.get(0).getContext("2d");

canvasElement.appendTo($(".game"));
}

function Tile(x, y, consumables, enemies, players, weapons) {
    this.x = x;
    this.y = y;
    this.consumables = consumables;
    this.enemies = enemies;
    this.players = players;
    this.weapons = weapons;
    this.color = "#7c5b51";
    this.draw = function() {
    if (this.players.length > 0) {
        canvas.fillStyle = "#0c9e20"
    } else { 
        canvas.fillStyle = this.color; 
    }
    if (this.enemies.length > 0) {
        canvas.fillStyle = "#cc0606"
    }
    if (this.weapons.length || this.consumables.length > 0) {
        canvas.fillStyle = "#0061ff"
    }
    canvas.fillRect(this.x * 100, this.y * 100, 99, 99);
    }
}

function draw(tiles) {
  console.log(roomTiles)
  tiles.forEach(function(tile){tile.draw()})
}


var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function newGame(event) {
    event.preventDefault()
    token = getCookie('csrftoken');
    $(".start-game").remove()
    $.ajax({
        method: 'POST',
        xhrFields: {
            withCredentials: true
        },
        headers: {
            'X-CSRFToken': `${token}`
        },
        url: `${__API_URL__}room/new`,
        success: function (data) {
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
            draw(roomTiles)
        }
    });
}

function clearCanvas() {
    canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
}

function action(event) {
    event.preventDefault()
    data = {'data': event.target.actionInput.value}
    roomTiles = []
    console.log(roomTiles)
    $.ajax({
        method: 'POST',
        xhrFields: {
            withCredentials: true
        },
        data: data,
        headers: {
            'X-CSRFToken': `${token}`
        },
        url: `${__API_URL__}room/`,
        success: function (data) {
            console.log(data.message)
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
            clearCanvas()
            draw(roomTiles)
        }
    });
}

$(".start-game").on("click", newGame);
$(".action-form").on("submit", action);
