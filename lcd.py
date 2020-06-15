import os
import socket
import time
import logging
import threading
from queue import Queue

from app import create_app, db
from app.models import Measurement
from flask_migrate import Migrate

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    level=logging.INFO,
                    datefmt="%H:%M:%S")


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


logging.info("launching the app")
app = create_app(os.getenv('FLASK_CONFIG)') or 'default')
migrate = Migrate(app, db)

logging.info("running the app")

# app.run()
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, measurements=Measurements)

logging.info("finished startup")
