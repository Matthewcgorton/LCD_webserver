from flask import render_template, session, redirect, url_for, current_app, request, flash

from . import main
from .. import lcd_hardware
from .forms import lcd_set_form

import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

from .. import lcd_state
# from .. import lcd_state, task_queue

from .. import lcd_screen

#
# def post_msg_to_queue(msg):
#     # global task_queue
#
#     logging.info(f"View - posting message: {msg}")
#     print(f"View - posting message: {msg}")
#     # task_queue.put(msg)



@main.route('/')
def index():
    lcd_screen.post_msg_to_queue({'action': "test"})
    return render_template('index.html')


@main.route('/lcd/msg')
def lcd_message():
    return render_template('lcd.html', lines=lcd_state['msg'], local_hardware=current_app.config['LOCAL_HARDWARE'])


@main.route('/lcd/clear')
def lcd_clear_message():

    lcd_state['msg'] = {'line1': '', 'line2': '', 'line3': '', 'line4': ''}
    print("Clearing message")
    lcd_screen.post_msg_to_queue({'action': "redisplay"})
    flash('LCD clear message sent...')

    return render_template('lcd.html', msg=lcd_state['msg'], local_hardware=current_app.config['LOCAL_HARDWARE'])


@main.route('/lcd/set', methods=['GET', 'POST'])
def lcd_set_message():

    form = lcd_set_form(request.form)

    print(f"Request Methon: {request.method}")
    if request.method == 'POST':
        print(f"  Valid form? {form.validate()}")

        if form.validate():
            print("Processing submitted form data...")
            lcd_state['msg']['line1'] = form.line1.data
            lcd_state['msg']['line2'] = form.line2.data
            lcd_state['msg']['line3'] = form.line3.data
            lcd_state['msg']['line4'] = form.line4.data

            # lcd_string(lcd_state['msg']['line1'], 1)
            # lcd_string(lcd_state['msg']['line2'], 2)
            # lcd_string(lcd_state['msg']['line3'], 3)
            # lcd_string(lcd_state['msg']['line4'], 4)

            lcd_screen.post_msg_to_queue({'action': "redisplay"})
            flash('New message sent to LCD...')

            print("redirecting to GET display resource...")
            return redirect(url_for('main.lcd_message'))
        else:
            return render_template('lcd_set.html', form=form, local_hardware=current_app.config['LOCAL_HARDWARE'])

    else:  # was a GET message
        form = lcd_set_form()

        print("Displaying form for user data entry`...")
        form.line1.data = lcd_state['msg']['line1']
        form.line2.data = lcd_state['msg']['line2']
        form.line3.data = lcd_state['msg']['line3']
        form.line4.data = lcd_state['msg']['line4']
        return render_template('lcd_set.html', form=form)
