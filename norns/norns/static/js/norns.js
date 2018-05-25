let canvasWidth = 600;
let canvasHeight = 500;
let roomTiles = [];
let message
// const __API_URL__ = 'http://localhost:8000/api/v1/'
const __API_URL__ = 'https://norns.live/api/v1/'

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
        let image = new Image()
        if (this.enemies.length > 0) {
            stats(this.players)
            tile = 'static/assets/enemyfloortile.jpg'
            loadImages(tile, this.x * 100, this.y * 100)
        } else if (this.weapons.length || this.consumables.length > 0) {
            stats(this.players)
            tile = 'static/assets/lootfloortile.jpg'
            loadImages(tile, this.x * 100, this.y * 100)
        } else if (this.players.length > 0) {
            stats(this.players)
            tile = 'static/assets/playerfloortile.jpg'
            loadImages(tile, this.x * 100, this.y * 100)
        } else {
            stats(this.players)
            tile = 'static/assets/floortile.jpg'
            loadImages(tile, this.x * 100, this.y * 100)
        }

        if (this.players.length && this.enemies.length > 0) {
            $(".player-stats").append(`<li><b><i>Alert!</i><b></li>`)
            $(".player-stats").append(`<li><b><i>There are enemies on this tile!</i><b></li>`)

            this.enemies.forEach(function(enemy) {
                $(".player-stats").append(`<li>Name: ${enemy['name']}</li>`)
                $(".player-stats").append(`<li>Health: ${enemy['health']}</li>`)
            })
            console.log(this.enemies)
        }
    }
}

function loadImages(tile, x, y) {
    let image = new Image()
    image.addEventListener('load', function() {
        canvas.drawImage(image, x, y, 99, 99)
    }, false);
    image.src = tile
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
    $(".player-stats").empty()
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
            data.tiles.forEach(function(tile){
                roomTiles.push(new Tile(tile.x_coord, tile.y_coord, tile.consumables, tile.enemy_set, tile.player_set, tile.weapons))
            })
            clearCanvas()
            // console.log(data)
            $(".messages").text(data.message)
            draw(roomTiles)
        }
    });
}

function stats(players){
    players.forEach(function(player) {
        $( ".player-stats" ).append(`<li><h2>Player</h2></li>`)
        $( ".player-stats" ).append(`<li>Name: ${player['name']}</li>`)
        if (player['health'] < 1) {
            $( ".player-stats" ).append(`<li>Health:<b style="color: red;">Dead!</b></li>`)
        } else {
            $( ".player-stats" ).append(`<li>Health: ${player['health']}</li>`)
        }
        if (player['weapon'] != null){
            $( ".player-stats" ).append(`<li>Weapon: ${player['weapon']['name']}</li>`)
        }
        $( ".player-stats" ).append(`<li><h2>Inventory</h2></li>`)
        if (player['inventory']['consumables'] != null){
            player['inventory']['consumables'].forEach(function(consumable){
                $( ".player-stats" ).append(`<li>Consumable: ${consumable['name']}</li>`)
            })
        }
        if (player['inventory']['weapons'] != null){
            player['inventory']['weapons'].forEach(function(weapon){
                $( ".player-stats" ).append(`<li>Weapon: ${weapon['name']}</li>`)
            })
        }
    })
}

$(".join-game").on("click", joinGame);
$(".action-form").on("submit", action);
