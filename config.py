import os

basedir = os.path.abspath(os.path.dirname(__file__))
FLASK_APP = 'app.py'
FLASK_ENV = 'development'
FLASK_DEBUG = 1
CSRF_ENABLED = True
SECRET_KEY = 'YOLO_yolo-YOLO!'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
JSON_SORT_KEYS = False
URL = 'http://127.0.0.1:5000'

