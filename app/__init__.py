import socket

from flask import Flask, render_template, current_app
from flask_bootstrap import Bootstrap
from flask_script import Manager

from config import config

bootstrap = Bootstrap()
manager = Manager()


# ##################################################
# Global variables that represents the current state of the hardware
# ##################################################

lcd_state = {'msg': {'line1': "default msg line 1",
                     'line2': "default msg line 2",
                     'line3': "default msg line 3",
                     'line4': "default msg line 4"
                     },
             'backlight': 1}

bus = None  # place holder for hardware bus, if it is present



def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = "asdf"


    config[config_name].init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    from .main.lcd import lcd_init

    lcd_init(app.config['LOCAL_HARDWARE'])
    app.register_blueprint(main_blueprint)

    print("registering app from /app/__init__.py")

    # main_blueprint.lcd_string("adsa", 2)
    return app
