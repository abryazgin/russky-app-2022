#!/usr/bin/env bash

uvicorn \
    russky.app:app \
    --reload \
    --host 0.0.0.0
