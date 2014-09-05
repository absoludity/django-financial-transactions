SECRET_KEY='test'

STATIC_URL='/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test_financial_transactions.db',
    }
}

INSTALLED_APPS = [
    'categories',
    'django.contrib.contenttypes',
    'financial_transactions',
    'south',
]

MIDDLEWARE_CLASSES = []

# Support different currency formats.
USE_L10N = True
