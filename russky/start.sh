#!/usr/bin/env bash

uvicorn \
    russky.app:app \
    --host 0.0.0.0 \
    --port ${HTTP_PORT:-8080}
