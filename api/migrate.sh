#!/usr/bin/env bash
python migrate.py db init
python migrate.py db migrate -m "test"
python migrate.py db upgrade