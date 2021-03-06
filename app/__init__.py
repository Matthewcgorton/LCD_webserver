import socket

from flask import Flask, render_template, current_app
from flask_bootstrap import Bootstrap
from flask_script import Manager

import queue

# from .lcd.py import task_queue

from config import config

bootstrap = Bootstrap()
manager = Manager()


# ##################################################
# Global variables that represents the current state of the hardware
# ##################################################

lcd_state = {'msg': {'line1': "",
                     'line2': "",
                     'line3': "",
                     'line4': ""
                     },
             'backlight': 1}

lcd_initialized = False
bus = None  # place holder for hardware bus, if it is present


def create_app(config_name, outbound_queue):
    global task_queue

    task_queue = outbound_queue

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = "asdf"


    config[config_name].init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    # from .main.lcd_hardware import init_lcd

    # lcd_initialized = init_lcd(app.config['LOCAL_HARDWARE'])

    app.register_blueprint(main_blueprint)

    print("registering app from /app/__init__.py")

    task_queue.put({'action': 'initiatize'})

    # main_blueprint.lcd_string("adsa", 2)
    return app
