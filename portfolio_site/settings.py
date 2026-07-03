from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# SECRET KEY
# ---------------------------------------------------------------------------
_secret = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")

if not _secret:
    if DEBUG:
        import secrets
        _secret = secrets.token_hex(50)
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY environment variable must be set in production."
        )

SECRET_KEY = _secret

# ---------------------------------------------------------------------------
# HOSTS
# ---------------------------------------------------------------------------
_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(",") if h.strip()]

# ---------------------------------------------------------------------------
# SITE DOMAIN — single source of truth for canonical URLs, Open Graph tags,
# and the sitemap. Override with the SITE_DOMAIN env var if this ever moves.
# ---------------------------------------------------------------------------
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "shwetanshuc.com")
SITE_URL = f"https://{SITE_DOMAIN}"

# ---------------------------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    # Third-party
    "colorfield",
    # Project apps
    "apps.accounts",
    "apps.core",
    "apps.portfolio",
    "apps.testimonials",
    "apps.inquiries",
]

# ---------------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "apps.core.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.PublicVisitCounterMiddleware",
    "apps.core.middleware.PublicFormThrottleMiddleware",
    "apps.core.middleware.AdminLoginThrottleMiddleware",
]

ROOT_URLCONF = "portfolio_site.urls"

# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
                "apps.portfolio.context_processors.site_content",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_site.wsgi.application"

# ---------------------------------------------------------------------------
# DATABASES
# ---------------------------------------------------------------------------
_db_url = os.environ.get("DATABASE_URL", "")
_mysql_host = os.environ.get("MYSQL_HOST", "")

if _db_url:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(_db_url, conn_max_age=600)}
elif _mysql_host:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": _mysql_host,
            "NAME": os.environ.get("MYSQL_DB", "portfolio_site"),
            "USER": os.environ.get("MYSQL_USER", "root"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# ---------------------------------------------------------------------------
# STORAGE
# ---------------------------------------------------------------------------
# Media (user uploads) goes to S3 whenever AWS_STORAGE_BUCKET_NAME is set —
# required on Lightsail Container Service, since its container filesystem is
# ephemeral and wiped on every deploy/restart. Falls back to local disk for
# plain local development, same pattern as the DATABASE_URL fallback above.
USE_S3 = bool(os.environ.get("AWS_STORAGE_BUCKET_NAME"))

if USE_S3:
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
    AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "")
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_QUERYSTRING_AUTH = False
    # Namespaced under media/ so it doesn't mix with the db-backups/ prefix
    # the same bucket holds (see entrypoint.sh / scripts/db_backup.py).
    AWS_LOCATION = "media"

STORAGES = {
    "default": {
        "BACKEND": (
            "portfolio_site.storage.ResizingS3Storage"
            if USE_S3 else
            "portfolio_site.storage.ResizingFileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# STATIC & MEDIA
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("old-miller", BASE_DIR / "old-millerpiano-site"),
]

if USE_S3:
    _s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    MEDIA_URL = f"https://{_s3_domain}/{AWS_LOCATION}/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------------
# CACHES
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "master-template-cache",
    }
}

# ---------------------------------------------------------------------------
# INTERNATIONALISATION
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# DEFAULT PK
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "portfolio_site.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# ---------------------------------------------------------------------------
# ENSURE MEDIA DIR EXISTS (local filesystem storage only — S3 needs no dir)
# ---------------------------------------------------------------------------
if not USE_S3:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
