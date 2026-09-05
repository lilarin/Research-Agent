FROM python:3.14-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock /app/

FROM base AS api

RUN uv sync --frozen --no-dev --no-group worker

COPY main.py ./
COPY app ./app
COPY src ./src

CMD ["uv", "run", "--no-sync", "python", "main.py"]

FROM base AS worker

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync --frozen --no-dev --group worker

COPY main.py ./
COPY app ./app
COPY src ./src

CMD ["uv", "run", "--no-sync", "arq", "app.worker.WorkerSettings"]
