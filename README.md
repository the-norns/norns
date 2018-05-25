# The Norns

**Authors**:
- Kat Cosgrove [GitHub](https://github.com/katcosgrove) | [LinkedIn](https://www.linkedin.com/in/katcosgrove/)
- Adam Grandquist [GitHub](https://github.com/grandquista) | [LinkedIn](https://www.linkedin.com/in/grandquista/)
- David Snowberger [GitHub](https://github.com/dsnowb) | [Linkedin](https://www.linkedin.com/in/dsnowberger)

**Version**: 0.1.0
[![Build Status](https://travis-ci.org/the-norns/norns.svg?branch=master)](https://travis-ci.org/the-norns/norns)
[![Coverage Status](https://coveralls.io/repos/github/the-norns/norns/badge.svg?branch=master)](https://coveralls.io/github/the-norns/norns?branch=master)

## Overview
The Norns is a top-down, turned-based, 90's inspired dungeon crawler. Adventure in style! Find cool weapons only to be slain by... err... and then slay mythical beasts!

## Architecture
This app is written using Python 3.6 using Django, Postgres, HTML, and CSS

## Installation

1. Clone https://github.com/the-norns/norns

2. pip install -r requirments.txt

3. create postgres db

4. set up local environmental variables in your environment

```
# Project-specific env variables
export SECRET_KEY='<your secret key>'
export DB_NAME='<db name>'
export DB_USER=''
export DB_PASSWORD=''
export DB_HOST='localhost'
```

5. In project directory (`norns`) run:

`./manage.py runserver` The server should now be running on localhost:8000

## Routes

- `/` Home view with story and game
  - GET: ```json
  ```
  - RESPONSE: ```html
  <!DOCTYPE html>
  <html lang="en" dir="ltr">
  ...
  <html />
  ```
- `/about/` About view with author information
  - GET: ```json
  ```
  - RESPONSE: ```html
  <!DOCTYPE html>
  <html lang="en" dir="ltr">
  ...
  <html />
  ```
- `/accounts/*` Endpoints for django registration and login
- `/admin/*` Endpoints for admin database CRUD operations
- `/api/v1/gear/weapon/<int>` Read information for weapon
  - GET: ```json
  ```
  - RESPONSE: ```json
  {}
  ```
- `/api/v1/room` Status of game
  - GET: ```json
  ```
  - RESPONSE: ```json
  {
  	"message": "",
  	"tiles": [
  		{
  			"x_coord": 0,
  			"y_coord": 0,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 1,
  			"y_coord": 3,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [
  				{
  					"id": 1,
  					"active": true,
  					"name": "adamgrandquist",
  					"max_health": 200,
  					"health": 200,
  					"combat_action": null,
  					"user": {
  						"id": 1
  					},
  					"inventory": {
  						"id": 5,
  						"weapons": [],
  						"consumables": []
  					},
  					"origin": {
  						"id": 1,
  						"grid_size": 5,
  						"round_start": null,
  						"room_north": null,
  						"room_east": null
  					},
  					"weapon": null,
  					"tile": {
  						"id": 9,
  						"looked": false,
  						"x_coord": 1,
  						"y_coord": 3,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 1,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 1,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 16,
  						"name": "Warg",
  						"health": 300
  					},
  					"inventory": {
  						"id": 1,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 17,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 1,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 4,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 2,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 11,
  						"name": "Dwarf",
  						"health": 150
  					},
  					"inventory": {
  						"id": 2,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 20,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 4,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		}
  	]
  }
  ```
- POST `/api/v1/room` Send current user command as `data` key
  - POST: ```json
  {"data": "<string user action>"}
  ```
  - RESPONSE: ```json
  {
  	"message": "",
  	"tiles": [
  		{
  			"x_coord": 0,
  			"y_coord": 0,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 1,
  			"y_coord": 3,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [
  				{
  					"id": 1,
  					"active": true,
  					"name": "adamgrandquist",
  					"max_health": 200,
  					"health": 200,
  					"combat_action": null,
  					"user": {
  						"id": 1
  					},
  					"inventory": {
  						"id": 5,
  						"weapons": [],
  						"consumables": []
  					},
  					"origin": {
  						"id": 1,
  						"grid_size": 5,
  						"round_start": null,
  						"room_north": null,
  						"room_east": null
  					},
  					"weapon": null,
  					"tile": {
  						"id": 9,
  						"looked": false,
  						"x_coord": 1,
  						"y_coord": 3,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 1,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 1,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 16,
  						"name": "Warg",
  						"health": 300
  					},
  					"inventory": {
  						"id": 1,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 17,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 1,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 4,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 2,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 11,
  						"name": "Dwarf",
  						"health": 150
  					},
  					"inventory": {
  						"id": 2,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 20,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 4,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		}
  	]
  }
  ```
- `/api/v1/room/new` Route to create game
  - POST: ```json
  ```
  - RESPONSE: ```json
  {
  	"message": "",
  	"tiles": [
  		{
  			"x_coord": 0,
  			"y_coord": 0,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 1,
  			"y_coord": 3,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [
  				{
  					"id": 1,
  					"active": true,
  					"name": "adamgrandquist",
  					"max_health": 200,
  					"health": 200,
  					"combat_action": null,
  					"user": {
  						"id": 1
  					},
  					"inventory": {
  						"id": 5,
  						"weapons": [],
  						"consumables": []
  					},
  					"origin": {
  						"id": 1,
  						"grid_size": 5,
  						"round_start": null,
  						"room_north": null,
  						"room_east": null
  					},
  					"weapon": null,
  					"tile": {
  						"id": 9,
  						"looked": false,
  						"x_coord": 1,
  						"y_coord": 3,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			],
  			"enemy_set": []
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 1,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 1,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 16,
  						"name": "Warg",
  						"health": 300
  					},
  					"inventory": {
  						"id": 1,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 17,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 1,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		},
  		{
  			"x_coord": 3,
  			"y_coord": 4,
  			"consumables": [],
  			"weapons": [],
  			"player_set": [],
  			"enemy_set": [
  				{
  					"id": 2,
  					"name": "Unnamed",
  					"health": 10,
  					"enemy_type": {
  						"id": 11,
  						"name": "Dwarf",
  						"health": 150
  					},
  					"inventory": {
  						"id": 2,
  						"weapons": [],
  						"consumables": []
  					},
  					"weapon": null,
  					"tile": {
  						"id": 20,
  						"looked": false,
  						"x_coord": 3,
  						"y_coord": 4,
  						"desc": "",
  						"room": {
  							"id": 1,
  							"grid_size": 5,
  							"round_start": null,
  							"room_north": null,
  							"room_east": null
  						},
  						"consumables": [],
  						"weapons": []
  					},
  					"abilities": []
  				}
  			]
  		}
  	]
  }
  ```
- `/api/v1/tile/<int>` Read information for tile
- `/store/` Store view with microtransactions
  - GET: ```json
  ```
  - RESPONSE: ```html
  <!DOCTYPE html>
  <html lang="en" dir="ltr">
  ...
  <html />
  ```
- `/store/<str>` Post route for purchasing
  - `/store/safe` Buy a room clear
  - `/store/thor` Buy Mjolnir
  - `/store/walker` Buy a weapon
  - POST: `<stripe data>`
  - RESPONSE: `<301 redirect '/' on success>`
- `/login/*` Endpoints for Django rest token authentication

## Change Log
- 25 May 2018 - Clean up and present
- 24 May 2018 - Style game UI
- 23 May 2018 - Add dynamic creation to room and loot
- 22 May 2018 - Set up start state and actions
- 21 May 2018 - Create models for players, game, enemy
- 20 May 2018 - Wireframe front end, extend deployment to Docker
- 19 May 2018 - Project Initialized

## Resources
- Django
  - REST framework
  - Background tasks
  - TDD
- Amazon AWS
- Docker
