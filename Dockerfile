# syntax=docker/dockerfile:1.7

# ---- Stage 1: build the React/Vite frontend --------------------------------
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Python runtime serving API + static files --------------------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ ./
COPY --from=frontend-build /frontend/dist ./static

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /data/media \
    && chown -R app:app /data /srv
USER app

ENV STATIC_DIR=/srv/static \
    MEDIA_DIR=/data/media \
    PORT=8000
EXPOSE 8000

# Migrate, then serve. $PORT is honoured by Render/Railway.
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
