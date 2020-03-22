import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@127.0.0.1:3306/blogdb'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blogdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_POOL_RECYCLE = 280
    # SQLALCHEMY_POOL_SIZE = 20
    SECRET_KEY = 'something very secret'
    SECURITY_SEND_REGISTER_EMAIL = False

    ### Flask Security

    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_LOGIN_URL = '/login'

    ### Heroku

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')