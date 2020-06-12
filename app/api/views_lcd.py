from flask import render_template, session, redirect, url_for, current_app, request, make_response
from flask_httpauth import HTTPBasicAuth

from .. import lcd_state, task_queue
from . import api

import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

from .. import lcd_state, task_queue
# from .. import lcd_state


def post_msg_to_queue(msg):
    global task_queue

    logging.info(f"View - posting message: {msg}")
    task_queue.put(msg)



auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(user, password):
    print(f"User: {user}, Password: {password}")
    if user != '':
        return True
    else:
        return False


@api.route('/lcd/msg')
def lcd_message():
    logging.info(f"Accept data: {request}\n{request.accept_mimetypes}\n{request.accept_mimetypes.accept_json}")
    if not request.accept_mimetypes.accept_json:
        return render_template('500.html'), 500

    response = make_response({'status': 'success', 'msg': lcd_state['msg']})
    response.status_code = 200
    return response
    # return render_template('api-lcd.html', lines=lcd_state['msg'], local_hardware=current_app.config['LOCAL_HARDWARE'])


@api.route('/lcd/clear')
@auth.login_required
def lcd_clear_message():

    lcd_state['msg'] = {'line1': '', 'line2': '', 'line3': '', 'line4': ''}
    post_msg_to_queue({'action': "redisplay"})

    response = make_response({'status': 'success', 'msg': lcd_state['msg']})
    response.status_code = 200
    return response

    # return render_template('lcd.html', msg=lcd_state['msg'], local_hardware=current_app.config['LOCAL_HARDWARE'])


@api.route('/lcd/set', methods=['POST'])
def lcd_set_message():

    post_data = request.json

    lcd_update = False
    if 'msg' in post_data.keys():

        if 'line1' in post_data['msg'].keys():
            lcd_state['msg']['line1'] = post_data['msg']['line1']
            lcd_update = True

        if 'line2' in post_data['msg'].keys():
            lcd_state['msg']['line2'] = post_data['msg']['line2']
            lcd_update = True

        if 'line3' in post_data['msg'].keys():
            lcd_state['msg']['line3'] = post_data['msg']['line3']
            lcd_update = True

        if 'line4' in post_data['msg'].keys():
            lcd_state['msg']['line4'] = post_data['msg']['line4']
            lcd_update = True

    if lcd_update:
        post_msg_to_queue({'action': "redisplay"})

    response = make_response({'status': 'success', 'msg': "request queued", 'request_data': post_data})
    response.status_code = 200
    return response
