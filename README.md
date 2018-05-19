# The Norns

**Authors**: 
- Kat Cosgrove [Git Hub](https://github.com/katcosgrove) | [LinkedIn](https://www.linkedin.com/in/katcosgrove/)
- Asa Katida [Git Hub](https://github.com/asakatida) | [LinkedIn](https://www.linkedin.com/in/asakatida/)
- David Snowberger [Git Hub](https://github.com/dsnowb) | [Linkedin](https://www.linkedin.com/in/dsnowberger)

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

TBD

## Change Log
19 May 2018 - Project Initialized

## Resources
- Django
- Amazon AWS
