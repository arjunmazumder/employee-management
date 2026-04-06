

from pathlib import Path
from datetime import timedelta
import os
import pymysql




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$hrkuf=n*9no2d477g&_fujwnq4)_w0v)7jkkem4vff^*0gi)y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.User'



# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'djoser',
    'users',
    'product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saleZen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'saleZen.wsgi.app'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'softzen1_zenuserdb',
#         'USER': 'softzen1-arjun',
#         'PASSWORD': 'Arjun1234*',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'softzen1_saledb',
#         'USER': 'softzen1_salezenuser',
#         'PASSWORD': 'Arjun37912',
#         'HOST': '144.79.133.221',
#         'PORT': '3306',
#     }
# }


#without pooler
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'Sq2W2dy4hf1CmHMu',
#         'HOST': 'db.ualupjqgxnagzilprjci.supabase.co',
#         'PORT': '5432',
#     }
# }


#with transjation pooler

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres.ualupjqgxnagzilprjci',
#         'PASSWORD': 'Sq2W2dy4hf1CmHMu',
#         'HOST': 'aws-1-ap-southeast-1.pooler.supabase.com',
#         'PORT': '6543',
#         'OPTIONS': {
#             'connect_timeout': 10,
#         }
#     }
# }


#session

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'mysql.connector.django',
        'NAME': 'postgres',
        'USER': 'postgres.ualupjqgxnagzilprjci', 
        'PASSWORD': 'Sq2W2dy4hf1CmHMu',          
        'HOST': 'aws-1-ap-northeast-1.pooler.supabase.com', 
        'PORT': '5432',                          
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

pymysql.install_as_MySQLdb()

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
#    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_TYPES': ('Bearer',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

DJOSER = {
    # 'EMAIL_FRONTEND_PROTOCOL': config('FRONTEND_PROTOCOL'),
    # 'EMAIL_FRONTEND_DOMAIN': config('FRONTEND_DOMAIN'),
    # 'EMAIL_FRONTEND_SITE_NAME': 'PhiMart',
    # 'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': 'activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserSerializer'
    },
}

