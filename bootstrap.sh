#! /usr/bin/env bash

set -ex

PORT=${TCE_PRIMARY_PORT:-5500}

exec python3 -m gunicorn -k sync app:app -t 300 --keep-alive 30 -w 6 --limit-request-field_size 0 -b "[::]:$PORT"

