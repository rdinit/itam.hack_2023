#!/bin/sh
python3 time_sleep.py
flask db init
flask db migrate
flask db upgrade
export FILL_DB=1
flask run --port=80 --host 0.0.0.0
