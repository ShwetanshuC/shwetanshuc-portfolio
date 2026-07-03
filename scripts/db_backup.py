"""
Uploads/downloads the MySQL "hard autosave" dump to/from S3.

Used by entrypoint.sh: the dump itself is produced with `mysqldump` in the
shell script (nothing Python-specific about that part) — this just handles
the S3 transfer, since boto3 is already a project dependency and pulling in
the full awscli package just for `s3 cp` would bloat the image for no reason.

Usage:
    python3 scripts/db_backup.py upload   /tmp/autosave.sql.gz
    python3 scripts/db_backup.py download /tmp/restore.sql.gz   # exit 1 if none exists yet
"""
import os
import sys

BACKUP_KEY = "db-backups/latest.sql.gz"


def _client():
    import boto3
    return boto3.client("s3", region_name=os.environ.get("AWS_S3_REGION_NAME", "us-east-1"))


def upload(path):
    bucket = os.environ["AWS_STORAGE_BUCKET_NAME"]
    _client().upload_file(path, bucket, BACKUP_KEY)
    print(f"Uploaded backup to s3://{bucket}/{BACKUP_KEY}")


def download(path):
    bucket = os.environ["AWS_STORAGE_BUCKET_NAME"]
    try:
        _client().download_file(bucket, BACKUP_KEY, path)
        print(f"Downloaded backup from s3://{bucket}/{BACKUP_KEY}")
        return True
    except Exception as e:
        print(f"No existing backup to restore ({e})")
        return False


if __name__ == "__main__":
    action, path = sys.argv[1], sys.argv[2]
    if action == "upload":
        upload(path)
    elif action == "download":
        sys.exit(0 if download(path) else 1)
    else:
        raise SystemExit(f"Unknown action: {action}")
