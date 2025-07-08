FROM python:3.12-slim

# Install Rust and system build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files first
COPY pyproject.toml poetry.lock ./

# Prevent Poetry from using virtualenvs and install dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root
 
# Copy the full app
COPY . .

# Expose the default FastAPI port
EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
