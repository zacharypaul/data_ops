FROM python:3.9-slim

WORKDIR /app

# Install minimal dependencies - only what we need for the simple server
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Only install required packages for the simple server
RUN pip install --no-cache-dir fastapi uvicorn pydantic

COPY . .

CMD ["uvicorn", "simple_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 