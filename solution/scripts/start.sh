#!/bin/sh

PORT=${SERVER_PORT:-8080}

uvicorn app.main:app_router --host 0.0.0.0 --port "$PORT" --workers 3
