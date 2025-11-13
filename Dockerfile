FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install LumenQA in development mode
RUN pip install --no-cache-dir -e .

# Create alias for lumen command
RUN echo '#!/bin/bash\npython -m lumenqa "$@"' > /usr/local/bin/lumenqa && \
    chmod +x /usr/local/bin/lumenqa

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Default command shows help
CMD ["lumen", "--help"]
