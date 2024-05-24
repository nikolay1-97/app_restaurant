#!/bin/bash

cd app

alembic upgrade head

python clear_database.py

python database_entry.py

gunicorn main:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000