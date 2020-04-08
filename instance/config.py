"""
    This module sets up the configurations for running the app
"""
import os


class Config:
    """
        This defines the base config class
    """

    URL= 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
    JWT_KEY = '76trdcv213456(*&^$%%%khJf)EWRFDG3245666uyYR%IUn)(*&TG'
    JWT_TIME = 11234567
    DEBUG = False
    BUNDLE_ERRORS = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or JWT_KEY
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES') or JWT_TIME
    DATABASE_URL = os.getenv('DATABASE_URL') or URL
    DB_NAME = os.getenv('DB_NAME')


class HerokuConfig(Config):
    """
        Thsi defines the development environment of the app
    """
    URL= 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
    JWT_KEY = '76trdcv213456(*&^$%%%khJf)EWRFDG3245666uyYR%IUn)(*&TG'
    JWT_TIME = 11234567
    PROPAGATE_EXEPTIONS = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL') or URL
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or JWT_KEY
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES') or JWT_TIME


class DevelopmentConfig(Config):
    """
        Thsi defines the development environment of the app
    """
    URL= 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
    JWT_KEY = '76trdcv213456(*&^$%%%khJf)EWRFDG3245666uyYR%IUn)(*&TG'
    JWT_TIME = 11234567
    PROPAGATE_EXEPTIONS = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL') or URL
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or JWT_KEY
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES') or JWT_TIME


class TestingConfig(Config):
    """
        This defines the testing environment for the app
    """
    URL= 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
    JWT_KEY = '76trdcv213456(*&^$%%%khJf)EWRFDG3245666uyYR%IUn)(*&TG'
    JWT_TIME = 11234567
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL') or URL
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or JWT_KEY
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES') or JWT_TIME



class ProductionConfig(Config):
    """
        This defines the production environment fro the app
    """
    URL= 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
    JWT_KEY = '76trdcv213456(*&^$%%%khJf)EWRFDG3245666uyYR%IUn)(*&TG'
    JWT_TIME = 11234567
    DEBUG = False
    TESTING = False
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = os.getenv('DATABASE_URL') or URL
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or JWT_KEY
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES') or JWT_TIME


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': HerokuConfig
}