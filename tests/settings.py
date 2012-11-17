from {{ project_name }}.settings import *

DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
PASSWORD_HASHERS = ['django.contrib.auth.hashers.SHA1PasswordHasher']
STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
