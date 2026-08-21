"""
Django settings for the HY-FY Technology website.

Security notes
---------------
Every secret / environment-specific value is pulled from environment
variables (see .env-demo for the full list). Never commit a real .env
file to version control.
"""

from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
# Read .env if present (safe no-op in production where real env vars are set)
environ.Env.read_env(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Core / Security
# ---------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure-CHANGE-ME-IN-PRODUCTION")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

SITE_URL = env("SITE_URL", default="http://127.0.0.1:8000")
SITE_NAME = "HY-FY Technology"

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    "core",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hy_fy_project.urls"

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
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "hy_fy_project.wsgi.application"
ASGI_APPLICATION = "hy_fy_project.asgi.application"

# ---------------------------------------------------------------------------
# Database
# Development default: SQLite3
# Production: set DATABASE_URL, e.g.
#   postgres://USER:PASSWORD@HOST:PORT/NAME
# ---------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & Media files
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Security hardening (production values controlled via env so DEBUG/local
# development is not broken by forced HTTPS redirects, etc.)
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=not DEBUG)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0 if DEBUG else 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# Trust the reverse proxy (Nginx) for HTTPS detection
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Admin URL can be changed via env so /admin/ is not guessable in production
DJANGO_ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# ---------------------------------------------------------------------------
# Email (Resend). Django's SMTP backend is used with Resend's SMTP relay by
# default; RESEND_API_KEY is used by core/email_utils.py for the API-based
# send (recommended). Falls back to console output when DEBUG and no key set.
# ---------------------------------------------------------------------------
RESEND_API_KEY = env("RESEND_API_KEY", default="")
ENQUIRY_FROM_EMAIL = env("ENQUIRY_FROM_EMAIL", default="enquiries@hyfytechnology.com")
ENQUIRY_TO_EMAIL = env("ENQUIRY_TO_EMAIL", default="hyfy.technology@hotmail.com")

if RESEND_API_KEY and not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="smtp.resend.com")
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="resend")
    EMAIL_HOST_PASSWORD = RESEND_API_KEY
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = ENQUIRY_FROM_EMAIL

# ---------------------------------------------------------------------------
# Third-party integration keys (front-end only, safe to expose in templates)
# ---------------------------------------------------------------------------
GOOGLE_MAPS_EMBED_URL = env("GOOGLE_MAPS_EMBED_URL", default="")
GOOGLE_ANALYTICS_ID = env("GOOGLE_ANALYTICS_ID", default="")
WHATSAPP_NUMBER = env("WHATSAPP_NUMBER", default="919750641426")
COMPANY_PHONE = env("COMPANY_PHONE", default="9750641426")
COMPANY_EMAIL = env("COMPANY_EMAIL", default="hyfy.technology@hotmail.com")
COMPANY_ADDRESS = env(
    "COMPANY_ADDRESS",
    default="New No. 30, Old No. 795, 1st Floor, Trunk Road, Poonamallee, Chennai, Tamil Nadu - 600056",
)

# ---------------------------------------------------------------------------
# Caching (used for simple rate-limiting of the enquiry form)
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# ---------------------------------------------------------------------------
# Logging - surfaces security-relevant events (blocked hosts, 4xx/5xx, etc.)
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# File upload limits (defence against oversized uploads via Django Admin)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
