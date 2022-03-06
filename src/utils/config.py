# encoding=utf-8
from environs import Env

env = Env()
env.read_env()


class AppConfig(object):

    SQLALCHEMY_DATABASE_URI = f"postgresql://{env.str('DB_USERNAME')}:{env.str('DB_PASSWORD')}@{env.str('DB_HOST')}/{env.str('DB_NAME')}"
    SECRET_KEY = env.str("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
