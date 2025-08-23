from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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