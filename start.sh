#!/bin/bash
gunicorn app.main:app \
  -w ${WEB_CONCURRENCY:-2} \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --timeout 120 \
  --graceful-timeout 30 \
  --keep-alive 5 \
  --access-logfile -