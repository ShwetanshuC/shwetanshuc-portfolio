#!/bin/sh
set -e

# ---------------------------------------------------------------------------
# Self-hosted MySQL, persisted across deployments via S3 "hard autosave"
# (no separate managed database service — matches the Southern Park setup).
#
# Lightsail Container Service wipes the container filesystem on every
# deploy/restart, so MySQL's own data directory can't be trusted to survive.
# Instead: restore the latest full dump from S3 on boot, take a full dump
# and re-upload it periodically AND on shutdown (SIGTERM), overwriting the
# same S3 key each time. "Hard" meaning a full overwrite of one backup file,
# not incremental — simple, but the tradeoff is any writes between the last
# autosave and an ungraceful crash are lost. Acceptable for this site's
# traffic; not a substitute for real point-in-time backups at higher stakes.
# ---------------------------------------------------------------------------

MYSQL_DATA_DIR=/var/lib/mysql
DB_NAME="${MYSQL_DB:-portfolio_site}"

if [ ! -d "$MYSQL_DATA_DIR/mysql" ]; then
  echo "Initializing MySQL data directory..."
  mariadb-install-db --user=mysql --datadir="$MYSQL_DATA_DIR" >/dev/null
fi

echo "Starting MySQL..."
mysqld_safe --datadir="$MYSQL_DATA_DIR" &
MYSQL_PID=$!

echo "Waiting for MySQL to accept connections..."
until mysqladmin ping --silent 2>/dev/null; do
  sleep 1
done

mysql -uroot <<-SQL
  CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`;
  CREATE USER IF NOT EXISTS '${MYSQL_USER:-appuser}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
  GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${MYSQL_USER:-appuser}'@'localhost';
  FLUSH PRIVILEGES;
SQL

if [ -n "$AWS_STORAGE_BUCKET_NAME" ]; then
  echo "Checking S3 for an existing database backup..."
  if python3 scripts/db_backup.py download /tmp/restore.sql.gz; then
    echo "Restoring database from backup..."
    gunzip -c /tmp/restore.sql.gz | mysql -uroot "$DB_NAME"
    rm -f /tmp/restore.sql.gz
  else
    echo "No existing backup — starting with an empty database."
  fi
else
  echo "AWS_STORAGE_BUCKET_NAME not set — skipping restore, no autosave will run."
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# First-ever boot (or a boot with no S3 backup to restore): the DB has
# tables but no rows. Load the real site content baked into the image so
# the site isn't blank. Once loaded, it lives on via the S3 autosave from
# then on — this only ever fires once.
if [ -f fixtures/production_seed.json ]; then
  PROJECT_COUNT=$(python manage.py shell -c "from apps.portfolio.models import Project; print(Project.objects.count())" 2>/dev/null | tail -1)
  if [ "$PROJECT_COUNT" = "0" ]; then
    echo "Empty database — loading production_seed.json..."
    python manage.py loaddata fixtures/production_seed.json
  fi
fi

save_now() {
  if [ -n "$AWS_STORAGE_BUCKET_NAME" ]; then
    mysqldump -uroot "$DB_NAME" | gzip > /tmp/autosave.sql.gz
    python3 scripts/db_backup.py upload /tmp/autosave.sql.gz
    rm -f /tmp/autosave.sql.gz
  fi
}

autosave_loop() {
  while true; do
    sleep "${DB_AUTOSAVE_INTERVAL:-600}"
    echo "Autosaving database to S3..."
    save_now
  done
}

if [ -n "$AWS_STORAGE_BUCKET_NAME" ]; then
  autosave_loop &
  AUTOSAVE_PID=$!
fi

shutdown() {
  # The platform's SIGTERM-to-SIGKILL grace window is finite and outside our
  # control — if the dump+upload gets squeezed out by a graceful gunicorn
  # drain or a clean mysqld shutdown eating the same window, the save that
  # actually matters never happens. So: save first, immediately, before
  # anything else — then kill the rest without waiting for a clean exit.
  echo "Container stopping — running final hard autosave..."
  save_now
  echo "Autosave done — shutting down."
  [ -n "$AUTOSAVE_PID" ] && kill -9 "$AUTOSAVE_PID" 2>/dev/null
  [ -n "$GUNICORN_PID" ] && kill -9 "$GUNICORN_PID" 2>/dev/null
  [ -n "$MYSQL_PID" ] && kill -9 "$MYSQL_PID" 2>/dev/null
  exit 0
}
trap shutdown TERM INT

echo "Starting gunicorn..."
gunicorn portfolio_site.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - &
GUNICORN_PID=$!

wait "$GUNICORN_PID"
