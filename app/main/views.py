from flask import render_template, session, redirect, url_for, current_app, request

from . import main
from .forms import lcd_set_form


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/lcd/msg')
def lcd_message():
    return render_template('lcd.html', lines=current_app.config['LCD_DISPLAY']['msg'])


@main.route('/lcd/clear')
def lcd_clear_message():

    current_app.config['LCD_DISPLAY']['msg'] = {'line1': '', 'line2': '', 'line3': '', 'line4': ''}
    return render_template('lcd.html', msg=current_app.config['LCD_DISPLAY']['msg'])


@main.route('/lcd/set', methods=['GET', 'POST'])
def lcd_set_message():
    form = lcd_set_form(request.form)

    # app.logger.debug('A value for debugging')
    # app.logger.warning('A warning occurred (%d apples)', 42)
    # app.logger.error('An error occurred')

    print(f"Request Methon: {request.method}")
    if request.method == 'POST':
        print(f"  Valid form? {form.validate()}")

        if form.validate():
            print("Processing submitted form data...")
            current_app.config['LCD_DISPLAY']['msg']['line1'] = form.line1.data
            current_app.config['LCD_DISPLAY']['msg']['line2'] = form.line2.data
            current_app.config['LCD_DISPLAY']['msg']['line3'] = form.line3.data
            current_app.config['LCD_DISPLAY']['msg']['line4'] = form.line4.data

            print("redirecting to GET display resource...")
            return redirect(url_for('main.lcd_message'))
        else:
            return render_template('lcd_set.html', form=form)

    else:  # was a GET message
        form = lcd_set_form()

        print("Displaying form for user data entry`...")
        form.line1.data = current_app.config['LCD_DISPLAY']['msg']['line1']
        form.line2.data = current_app.config['LCD_DISPLAY']['msg']['line2']
        form.line3.data = current_app.config['LCD_DISPLAY']['msg']['line3']
        form.line4.data = current_app.config['LCD_DISPLAY']['msg']['line4']
        return render_template('lcd_set.html', form=form)
