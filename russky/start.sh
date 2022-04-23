#!/usr/bin/env bash

uvicorn \
    russky.app:app \
    --host 0.0.0.0 \
    --port 80
