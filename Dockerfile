FROM python:3.12-slim

# Prevent .pyc files and force stdout/stderr to be unbuffered (so logs show
# up immediately in `docker logs` / Lightsail's log viewer).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# libjpeg/zlib for Pillow, libpq for psycopg2 at runtime, mariadb-server for
# the self-hosted database (see entrypoint.sh for the S3 autosave/restore
# that gives it persistence across this container's ephemeral filesystem).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libpq5 \
    mariadb-server \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/lib/mysql /var/run/mysqld \
    && chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

# Lightsail Container Service health check hits this (see /healthz/ in urls.py).
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
