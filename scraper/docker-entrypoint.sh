#!/bin/bash

PYTHON=python3.6

${PYTHON} manage.py db init
${PYTHON} manage.py db migrate
${PYTHON} manage.py db upgrade

${PYTHON} manage.py runserver -h 0.0.0.0