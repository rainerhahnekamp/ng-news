# Dockerfile for OpenAI Whisper with ffmpeg
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Whisper from GitHub
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Keep container running for interactive use
CMD ["/bin/bash"]
