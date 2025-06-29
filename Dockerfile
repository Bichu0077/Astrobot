FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .


RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir --timeout=1800 -r requirements.txt


FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libopenblas-dev \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
COPY . .

EXPOSE 8000

ENV GROK_API_KEY="your_placeholder_key"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
