
# Builder stage
FROM public.ecr.aws/docker/library/python:3.12-bullseye AS builder

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry
RUN pip install poetry==1.8.0

# Set the working directory
WORKDIR /app

# Copy the application code and Poetry files
COPY . /app

# Install dependencies using Poetry and cache them
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# Runtime stage
FROM public.ecr.aws/docker/library/python:3.12-slim AS runtime

# Set environment variables for the virtual environment and PATH
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment and application code from the builder stage
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app using Uvicorn from the virtual environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
