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
    this.color = "#7c5b51";
    this.enemies = enemies;
    this.players = players;
    this.weapons = weapons;
    this.draw = function() {
    canvas.fillStyle = this.color;
    canvas.fillRect(this.x * 100, this.y * 100, 99, 99);
  }
}

function draw(tiles) {
<<<<<<< HEAD
  tiles.forEach(function(tile){tile.draw()})
}

=======
  console.log('draw function triggered')
  tiles.forEach(function(tile){tile.draw()})
}

function getToken(event) {
    console.log(event)
}

$(".login-form").on("submit", getToken);

>>>>>>> f9e3b1c2e9157a7d587a925e370288d29b3bcd86
// function newGame(event) {
//     event.preventDefault()
//     $(".start-game").remove()
//     $.post(`${__API_URL__}room/new`, function (data) {
//     data.tiles.forEach(function(tile){
//         roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
//     })
//   })
//     .then(console.log(roomTiles))
//     .then(() => draw(roomTiles))
// }
<<<<<<< HEAD
=======

>>>>>>> f9e3b1c2e9157a7d587a925e370288d29b3bcd86
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
<<<<<<< HEAD
    console.log(token)
=======
>>>>>>> f9e3b1c2e9157a7d587a925e370288d29b3bcd86
    $.ajax({
        method: 'POST',
        xhrFields: {
            withCredentials: true
        },
        headers: {
<<<<<<< HEAD
            'Authorization': 'Token' + token
        },
        url: `${__API_URL__}room/new`,
        success: function (data) {console.log(data)}
    });
=======
            'X-CSRFToken': `${token}`
        },
        url: `${__API_URL__}room/new`,
        success: function (data) {
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
        }
    });
    draw(roomTiles);let CANVAS_WIDTH = 600;
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
    this.color = "#7c5b51";
    this.enemies = enemies;
    this.players = players;
    this.weapons = weapons;
    this.draw = function() {
    canvas.fillStyle = this.color;
    canvas.fillRect(this.x * 100, this.y * 100, 99, 99);
  }
}

function draw(tiles) {
  console.log('draw function triggered')
  tiles.forEach(function(tile){tile.draw()})
}

function getToken(event) {
    console.log(event)
}

$(".login-form").on("submit", getToken);

// function newGame(event) {
//     event.preventDefault()
//     $(".start-game").remove()
//     $.post(`${__API_URL__}room/new`, function (data) {
//     data.tiles.forEach(function(tile){
//         roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
//     })
//   })
//     .then(console.log(roomTiles))
//     .then(() => draw(roomTiles))
// }
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
        }
    });
    draw(roomTiles);
}

function clearCanvas() {
    canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
}

function action(event) {
    event.preventDefault()
    console.log(event.target.action.value)
    $.post(`${__API_URL__}room`, function(data){
        console.log(data)
        data.tiles.forEach(function(tile){
            roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
        })
    })
    .then(() => draw(roomTiles))
}

$(".start-game").on("click", newGame);
$(".action-form").on("submit", action);

>>>>>>> f9e3b1c2e9157a7d587a925e370288d29b3bcd86
}

function clearCanvas() {
    canvas.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
}

function action(event) {
    event.preventDefault()
    console.log(event.target.action.value)
    $.post(`${__API_URL__}room`, function(data){
        console.log(data)
        data.tiles.forEach(function(tile){
            roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
        })
    })
    .then(() => draw(roomTiles))
}

$(".start-game").on("click", newGame);
$(".action-form").on("submit", action);
