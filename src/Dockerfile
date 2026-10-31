
# Use a lightweight Python 3.11 image.
FROM python:3.11-slim

# Set the application directory.
WORKDIR /code

# Prevent Python from writing bytecode and buffer logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first for better Docker layer caching.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY . .

# Create a non-root user and prepare the persistent data directory.
RUN useradd --create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /code /data

# Run the application without root privileges.
USER appuser

# Document the application port.
EXPOSE 8080

# Start FastAPI.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
