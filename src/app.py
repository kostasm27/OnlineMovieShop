# encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)
db = SQLAlchemy(app, session_options={"autocommit": False})

db.init_app(app)
from views import *




if __name__ == '__main__':
    app.run(debug=True)
