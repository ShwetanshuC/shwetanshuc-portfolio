"""
Streams S3-backed media through this app so every URL reads as this site's
own domain (shwetanshuc.com/media/...) instead of the raw S3 bucket domain.

Only used when USE_S3 is on (production). boto3 is already a dependency
either way (see portfolio_site/storage.py).
"""
from django.conf import settings
from django.http import FileResponse, Http404


def media_proxy(request, path):
    if not settings.USE_S3:
        raise Http404

    import boto3
    from botocore.exceptions import ClientError

    client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
    key = f"{settings.AWS_LOCATION}/{path}"

    try:
        obj = client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") in ("NoSuchKey", "404"):
            raise Http404
        raise

    response = FileResponse(
        obj["Body"],
        content_type=obj.get("ContentType", "application/octet-stream"),
    )
    if "ContentLength" in obj:
        response["Content-Length"] = obj["ContentLength"]
    response["Cache-Control"] = obj.get("CacheControl", "max-age=86400")
    return response
