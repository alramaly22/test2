"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv  # قم بإضافة هذه المكتبة لتحميل متغيرات البيئة
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Load environment variables from .env file
load_dotenv()  # قم بتحميل متغيرات البيئة من ملف .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-9p7go%z)ati3-l2ab&6f1o*4ezf3p!9!4ny$j$1m#1+u39&*4#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
ALLOWED_HOSTS.append('.vercel.app')

# Stripe API Key
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')  # قم بإضافة هذا المتغير لقراءة مفتاح Stripe API من متغيرات البيئة

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cart',
    'payment',
    'store',
    'cloudinary',  # ✅ أضف هذا
    'cloudinary_storage',  # ✅ أضف هذا
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = {

#     'default': {


#         'ENGINE': 'django.db.backends.postgresql',

#         'NAME': 'railway',

#         'USER': 'postgres',

#         'PASSWORD': 'CmCCbvbOCIOgmxbqmESqxxYUCcNErdRB',

#         'HOST': 'viaduct.proxy.rlwy.net',  # اسم المضيف
#         'PORT': '47172',

#     }


# }
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'dliwkyyog',
#     'API_KEY': '223659487284859',
#     'API_SECRET': 'HmQ8VWrqXOSkgADBQXahIK8Mjis'
# }
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

cloudinary.config( 
  cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key=os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = True  # تأمين الكوكيز على HTTPS
SESSION_COOKIE_HTTPONLY = True  # منع الوصول إلى الجلسة من JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # السماح بإرسال الجلسة بين الصفحات
SESSION_COOKIE_AGE = 86400  # الجلسة تبقى نشطة لمدة يوم واحد
SESSION_SAVE_EVERY_REQUEST = True  # حفظ الجلسة مع كل طلب
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # لا تحذف الجلسة عند إغلاق المتصفح
CSRF_COOKIE_SECURE = True


# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
