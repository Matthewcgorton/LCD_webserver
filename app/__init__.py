import socket
import os

from flask import Flask, render_template, current_app
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from .lcd_hardware import LCD_Hardware

import queue

# from .lcd.py import task_queue

from config import config

bootstrap = Bootstrap()
manager = Manager()
db = SQLAlchemy()

local_hardware_os_setting = os.getenv('LOCAL_HARDWARE')
if local_hardware_os_setting == "1":
    local_hardware_flag = True
else:
    local_hardware_flag = False

lcd_screen = LCD_Hardware(local_hardware=local_hardware_flag)

# bus = None  # place holder for hardware bus, if it is present


def create_app(config_name):
    # global task_queue
    #
    # task_queue = outbound_queue

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = "asdf"

    config[config_name].init_app(app)
    bootstrap.init_app(app)

    db.init_app(app)
    lcd_screen.initialize_lcd()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/1.0')

    print("registering app from /app/__init__.py")

    # task_queue.put({'action': 'initiatize'})

    # main_blueprint.lcd_string("adsa", 2)
    return app
