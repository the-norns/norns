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

5. In project directory run:

`./manage.py runserver` The server should now be running on localhost:8000

## Routes

- `/` Home view with story and game
- `/about/` About view with author information
- `/accounts/*` Endpoints for django registration and login
- `/admin/*` Endpoints for admin database CRUD operations
- `/api/v1/gear/weapon/<int>` Read information for weapon
- `/api/v1/room` Status of game
- POST `/api/v1/room` Send current user command as `data` key
- `/api/v1/room/new` Route to create game
- `/api/v1/tile/<int>` Read information for tile
- `/store/` Store view with microtransactions
- `/store/<str>` Post route for purchasing
- `/login/*` Endpoints for rest token authentication

## Change Log
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
