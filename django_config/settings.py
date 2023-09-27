from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-5@ql9az*d^lm58m1f!2k)9e+4iy2^1(&bp6h!jv0jghpivct=8"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "ckeditor",
    "ckeditor_uploader",
    "dev_otion_app.apps.DevOtionAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
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


LANGUAGE_CODE = "en-us"

LOCALE_PATHS = [
    str(BASE_DIR)+"/dev_otion_app/locale"
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_SLUGIFY_FILENAME = False
CKEDITOR_FILENAME_GENERATOR = 'django_config.utils.unique_filename'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    }
}