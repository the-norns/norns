let canvasWidth = 600;
let canvasHeight = 500;
let roomTiles = [];
let message
const __API_URL__ = 'http://localhost:8000/api/v1/'

let canvasElement = $("<canvas width='" + canvasWidth + 
                      "' height='" + canvasHeight + "'></canvas>");
let canvas = canvasElement.get(0).getContext("2d");

canvasElement.appendTo($(".game"));

function Tile(x, y, consumables, enemies, players, weapons) {
    this.x = x;
    this.y = y;
    this.consumables = consumables;
    this.enemies = enemies;
    this.players = players;
    this.weapons = weapons;
    this.color = "#7c5b51";
    this.draw = function() {
    if (this.enemies.length > 0) {
        canvas.fillStyle = "#cc0606"
    } else if (this.weapons.length || this.consumables.length > 0) {
        canvas.fillStyle = "#0061ff"
    } else if (this.players.length > 0) {
        canvas.fillStyle = "#0c9e20"
    } else { 
        canvas.fillStyle = this.color; 
    }
    canvas.fillRect(this.x * 100, this.y * 100, 99, 99);
    }
}

function draw(tiles) {
  clearCanvas()
  tiles.forEach(function(tile){tile.draw()})
}

function clearCanvas() {
    canvas.clearRect(0, 0, canvasWidth, canvasHeight);
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

// function newGame(event) {
//     event.preventDefault()
//     token = getCookie('csrftoken');
//     $(".start-buttons").remove()
//     $.ajax({
//         method: 'POST',
//         xhrFields: {
//             withCredentials: true
//         },
//         headers: {
//             'X-CSRFToken': `${token}`
//         },
//         url: `${__API_URL__}room/new`,
//         success: function (data) {
//             data.tiles.forEach(function(tile){
//                 roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
//             })
//             draw(roomTiles)
//         }
//     });
// }

function joinGame(event) {
    event.preventDefault()
    token = getCookie('csrftoken');
    $(".start-buttons").remove()
    $(".action-ul").show()
    $.ajax({
        method: 'GET',
        xhrFields: {
            withCredentials: true
        },
        headers: {
            'X-CSRFToken': `${token}`
        },
        url: `${__API_URL__}room`,
        success: function (data) {
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
            $(".messages").text(data.message)
            draw(roomTiles)
        }
    });
}

function action(event) {
    event.preventDefault()
    data = {'data': event.target.actionInput.value}
    $(".action-form")[0].reset();
    roomTiles = []
    $.ajax({
        method: 'POST',
        xhrFields: {
            withCredentials: true
        },
        data: data,
        headers: {
            'X-CSRFToken': `${token}`
        },
        url: `${__API_URL__}room`,
        success: function (data) {
            console.log(data.message)
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
            clearCanvas()
            $(".messages").text(data.message)
            draw(roomTiles)
        }
    });
}

// $(".start-game").on("click", newGame);
$(".join-game").on("click", joinGame);
$(".action-form").on("submit", action);
