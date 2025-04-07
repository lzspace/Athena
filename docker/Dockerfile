# ./docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY assistant_core /app/assistant_core
COPY tests /app/tests
COPY .env /app/.env

CMD ["pytest", "tests/"]