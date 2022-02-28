# encoding=utf-8
from environs import Env

env = Env()
env.read_env()


class AppConfig(object):

    SECRET_KEY = env.str("SECRET_KEY")
    TESTING = True
