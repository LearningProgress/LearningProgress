"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from django.utils.translation import ugettext_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'bootstrap3',
    'learningprogress.accounts',
    'learningprogress.progress',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'learningprogress.urls'

WSGI_APPLICATION = 'learningprogress.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('en', ugettext_lazy('English')),
    ('de', ugettext_lazy('German')))

LOCALE_PATHS = (os.path.join(BASE_DIR, 'learningprogress', 'locale'),)

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'learningprogress', 'static'),)

STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')


# Miscellaneous

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'learningprogress', 'templates'),)

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'home'


# Email
# https://docs.djangoproject.com/en/1.6/topics/email/

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_USE_TLS = True

# EMAIL_HOST =

# EMAIL_HOST_USER =

# EMAIL_HOST_PASSWORD =

# DEFAULT_FROM_EMAIL =

# EMAIL_SUBJECT_PREFIX =
