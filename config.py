# www/config.py
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dbapp.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'dev_key_please_change'
SESSION_COOKIE_NAME = 'user_sid'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

print("Database URI:", SQLALCHEMY_DATABASE_URI)