import sys
from os import environ 


class Config(object):
    # environmental variables are set in .env, for development purpoises
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY', "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91")
            
    SESSION_COOKIE_SECURE = True
    

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    # CSRF_ENABLED = environ.get('CSRF_ENABLED', False)
    
    # App name
    APP_NAME = environ.get('APP_NAME', "Zaladin 2")

class ProductionConfig(Config):
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False