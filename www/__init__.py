# www/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta

app = Flask(__name__)

# Конфигурация
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dbapp.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev_key_please_change'
app.config['SESSION_COOKIE_NAME'] = 'user_sid'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

db = SQLAlchemy(app)

# Импортируем блюпринт после инициализации db
from .routes import main
app.register_blueprint(main)

# Создаем таблицы
with app.app_context():
    db.create_all()