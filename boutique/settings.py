"""
Django settings for boutique project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

#MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = '/root/bwebsite/boutique/boutique/uploaded_images/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o4tlw8mywdc@+vrl-4s@tds4uim6cogl@v48_w=$1)b58ev+k_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'boutique_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'boutique.urls'

WSGI_APPLICATION = 'boutique.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#Template directories
#
TEMPLATE_DIRS = (
#    '/root/testsite/testsite/testsite/templates/',
    '/root/bwebsite/boutique/boutique/templates/',
)

#Uploaded Images
UploadedImages = BASE_DIR + '/boutique/uploaded_images/'

STATICFILES_DIRS = (
#    ( 'css', '/root/amiwebsite/boutique/boutique/templates/css/'),
#    ( 'fonts', '/root/amiwebsite/boutique/boutique/templates/fonts/'),
#    ( 'images', '/root/amiwebsite/boutique/boutique/templates/images/'),
    ( 'css',     BASE_DIR + '/boutique/templates/css/'),
    ( 'fonts',   BASE_DIR + '/boutique/templates/fonts/'),
    ( 'images',  BASE_DIR + '/boutique/templates/images/'),
    ( 'scripts', BASE_DIR + '/boutique/scripts/'),
    ( 'uploaded_images', BASE_DIR + '/boutique/uploaded_images/' ),
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
