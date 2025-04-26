FROM python:3.12-slim

LABEL authors="Igor Jakus <igorjakus@protonmail.com>"

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # video/audio processing (whisper)
    ffmpeg \

    # computer vision (opencv)
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libgl1 \

    # remove apt-get cache
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install uv and use it to install dependencies
RUN pip install --no-cache-dir uv && \
    uv sync

# Copy the rest of the application
COPY . /app

EXPOSE 8000
CMD ["fastapi", "dev", "backend/main.py"]
