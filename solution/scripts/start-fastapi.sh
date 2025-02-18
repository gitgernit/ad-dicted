#!/bin/sh

PORT=${SERVER_PORT:-8080}

uvicorn app.adapters.fastapi.main:fastapi_app --host 0.0.0.0 --port "$PORT" --workers 3
