from flask import render_template, redirect, url_for, current_app, request, flash

from . import main
from .. import lcd_hardware
from .forms import lcd_set_form

import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

from .. import lcd_screen


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/lcd/msg')
def lcd_message():
    print(lcd_screen.lcd_get_lines())
    return render_template('lcd.html',
                           lines=lcd_screen.lcd_get_lines(),
                           local_hardware=current_app.config['LOCAL_HARDWARE'])


@main.route('/lcd/clear')
def lcd_clear_message():

    print("Clearing message...")
    lcd_screen.lcd_clear()

    flash('LCD has been cleared')
    return redirect(url_for('main.lcd_message'))


@main.route('/lcd/reset')
def lcd_reset():

    print("initialized")
    flash('LCD has been reset')
    lcd_screen.lcd_reset()

    return redirect(url_for('main.lcd_message'))


@main.route('/lcd/set', methods=['GET', 'POST'])
def lcd_set_message():

    form = lcd_set_form(request.form)

    print(f"Request Methon: {request.method}")
    if request.method == 'POST':
        print(f"  Valid form? {form.validate()}")

        if form.validate():
            print("Processing submitted form data...")
            lcd_screen.lcd_update(form.line1.data, form.line2.data, form.line3.data, form.line4.data)

            flash('New message sent to LCD...')

            print("redirecting to GET display resource...")
            return redirect(url_for('main.lcd_message'))
        else:
            return render_template('lcd_set.html', form=form, local_hardware=current_app.config['LOCAL_HARDWARE'])

    else:  # was a GET request
        form = lcd_set_form()

        print("Displaying form for user data entry`...")
        form.line1.data = lcd_screen.lcd_get_line(1)
        form.line2.data = lcd_screen.lcd_get_line(2)
        form.line3.data = lcd_screen.lcd_get_line(3)
        form.line4.data = lcd_screen.lcd_get_line(4)

        return render_template('lcd_set.html', form=form, local_hardware=current_app.config['LOCAL_HARDWARE'])
