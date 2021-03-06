import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'maybe_secret'
    LOCAL_HARDWARE = os.environ.get('LOCAL_HARDWARE') or False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {'development': DevelopmentConfig,
          'prod': ProductionConfig,

          'default': DevelopmentConfig
          }
