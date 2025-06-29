FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libopenblas-dev \
    libgomp1 \
    zlib1g-dev \
    git \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.org/simple

RUN pip install --no-cache-dir --timeout=1800 -r requirements.txt


COPY . .

ENV GROK_API_KEY="your_placeholder_key"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--port", "8000"]
