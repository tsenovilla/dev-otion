from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

INSTALLED_APPS = [
    "ckeditor",
    "ckeditor_uploader",
    "dev_otion_app.apps.DevOtionAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites"
]

SITE_ID = 1

if DEBUG:
    from dotenv import load_dotenv
    load_dotenv()

    SECRET_KEY = "django-insecure-5@ql9az*d^lm58m1f!2k)9e+4iy2^1(&bp6h!jv0jghpivct=8"

    DATABASES = {
        "default":
        {
            "ENGINE":"django.db.backends.mysql",
            "HOST":os.environ["DB_HOST"],
            "NAME":os.environ["DB_NAME"],
            "USER":os.environ["DB_USER"],
            "PASSWORD":os.environ["DB_PASS"]
        }
    }

    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    MEDIA_URL = "media/"
    MEDIA_ROOT = os.path.join(BASE_DIR,'media')
else:
    import dj_database_url
    import sys

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","").split(",")

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    INSTALLED_APPS.append("storages")

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
            "level": "WARNING",
        },
    }

    if len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
        if os.getenv("DATABASE_URL", None) is None:
            raise Exception("DATABASE_URL environment variable not defined")
        DATABASES = {
            "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
        }

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = "dev-otion-files"
    AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_LOCATION = "static"
    STATIC_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = "django_config.storages.StaticStorage"
    MEDIA_URL = "%s/media/" % AWS_S3_ENDPOINT_URL
    DEFAULT_FILE_STORAGE = "django_config.storages.PublicMediaStorage"
    CKEDITOR_BASEPATH = "%s/dev-otion-files/static/ckeditor/ckeditor/" % AWS_S3_ENDPOINT_URL


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_config.middleware.CKEditorMiddleware"
]

ROOT_URLCONF = "django_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        }
    }
]

WSGI_APPLICATION = "django_config.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    }
]


LANGUAGE_CODE = "en"

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French'))
]

LOCALE_PATHS = [
    str(BASE_DIR)+"/dev_otion_app/locale"
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_SLUGIFY_FILENAME = False
CKEDITOR_FILENAME_GENERATOR = 'django_config.utils.unique_filename'
CKEDITOR_RESTRICT_BY_DATE = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    }
}