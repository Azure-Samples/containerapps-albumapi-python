
# Use a lightweight Python 3.11 image.
FROM python:3.11-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Microsoft ODBC Driver 18 for SQL Server.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    . /etc/os-release; \
    DEBIAN_VERSION="${VERSION_ID%%.*}"; \
    curl -fsSLo /tmp/packages-microsoft-prod.deb \
        "https://packages.microsoft.com/config/debian/${DEBIAN_VERSION}/packages-microsoft-prod.deb"; \
    dpkg -i /tmp/packages-microsoft-prod.deb; \
    rm /tmp/packages-microsoft-prod.deb; \
    apt-get update; \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql18 \
        libgssapi-krb5-2; \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
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
