#!/bin/bash
set -ex

# sleep 60

# --
# Poetry v.
# --
source /app/poetry-venv/bin/activate
cd /app/FN-Basic-Services

# --
# Waitng for ES
./wait_for_es.sh $ES_HOST

#poetry run uvicorn main:app --host=0.0.0.0 --port=7091 --workers 4
poetry run gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:7091 --workers 4