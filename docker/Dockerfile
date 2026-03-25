FROM python:3.11-slim

LABEL maintainer="Imasola"
LABEL description="OpenGen Worker — contribute compute to the distributed AI research system"

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir -e .

# The .env file must be mounted or environment variables must be set
# docker run --env-file .env opengen-worker

CMD ["python", "-m", "opengen.worker.client"]
