
# Use a lightweight Python 3.11 image.
FROM python:3.11-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:////data/albums.db

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY . .

# Create a non-root user and prepare the database directory.
RUN useradd --create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /code /data

USER appuser

EXPOSE 8080

# Initialize the database, seed it, then start FastAPI.
CMD ["sh", "-c", "alembic upgrade head && python -m app.init_db && exec uvicorn app.main:app --host 0.0.0.0 --port 8080"]
