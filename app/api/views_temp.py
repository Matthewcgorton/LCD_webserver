from flask import render_template, session, redirect, url_for, current_app, request, make_response, g
from flask_httpauth import HTTPBasicAuth

from ..models import Measurement, User, Location

# from .. import lcd_state, db
from .. import db
from . import api

import logging
import datetime

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

# from .. import lcd_state, task_queue
# # from .. import lcd_state
#
#
# def post_msg_to_queue(msg):
#     global task_queue
#
#     logging.info(f"View - posting message: {msg}")
#     task_queue.put(msg)
#


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(user, password):
    print(f"User: {user}, Password: {password}")
    if user != '':
        # g.user = 1
        # return True
        user = User.query.filter_by(login_name=user).first()
        print(f"User: {user}")
        if not user:
            return False
        g.user = user.id
        return True
    else:
        return False


@api.route('/temp/get')
def get_temp():
    logging.info(f"Accept data: {request}\n{request.accept_mimetypes}\n{request.accept_mimetypes.accept_json}")
    if not request.accept_mimetypes.accept_json:
        return render_template('500.html'), 500

    response = make_response({'status': 'success', 'msg': lcd_state['msg']})
    response.status_code = 200
    return response



@api.route('/temp/add', methods=['POST'])
@auth.login_required
def temp_add():

    post_data = request.json

    if 'value' in post_data.keys():
        new_measurement = Measurement(value=post_data['value'], created_by=g.user, created=datetime.datetime.now())
        db.session.add(new_measurement)

        db.session.commit()


    response = make_response({'status': 'success', 'msg': "request queued", 'request_data': post_data})
    response.status_code = 200
    return response
