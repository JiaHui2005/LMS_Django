from .base import *

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


DEBUG = True