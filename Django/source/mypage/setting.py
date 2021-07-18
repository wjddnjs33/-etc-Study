import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECRET_KEY = '!#^m5zja*vs!fbuz-#=r+geh$=n)_y@ux_u49xv!i7mpa5vxiz'


DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'server',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admin', # DB명
        'USER': 'postgres', # user
        'PASSWORD': 'password', # user 비밀번호
        'HOST': '127.0.0.1', # db 주소(IP)
        'PORT': '5432', # db 포트
    }
}


ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

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


EMAIL_HOST = 'smtp.gmail.com' 		 # 메일 호스트 서버
EMAIL_PORT = '587' 			 # 서버 포트
EMAIL_HOST_USER = 'teamus2r@gmail.com' 	 # 우리가 사용할 Gmail
EMAIL_HOST_PASSWORD = 'qwer1202@'	# 우리가 사용할 Gmail의 password
EMAIL_USE_TLS = True			 # TLS 보안 설정
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER




LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 