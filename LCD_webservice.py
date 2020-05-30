import socket

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_script import Manager

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required, length

# ################################################################################
# Utility functions
# ################################################################################


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


# ################################################################################
# Form Definitions
# ################################################################################

class lcd_set_form(FlaskForm):
    line1 = StringField('Line1', validators=[length(max=20)])
    line2 = StringField('Line2', validators=[length(max=20)])
    line3 = StringField('Line3', validators=[length(max=20)])
    line4 = StringField('Line4', validators=[length(max=20)])
    submit = SubmitField('submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = "asdf"

bootstrap = Bootstrap(app)
manager = Manager(app)

# with app.app_context():
#     print(current_app().name)
#
#     app.current_app.lcd = {'msg': ["default msg line 1",
#                                    "default msg line 2",
#                                    "default msg line 3",
#                                    "default msg line 4"
#                                    ],
#                            'backlight': 1}
#


lcd = {'msg': {'line1': "default msg line 1",
               'line2': "default msg line 2",
               'line3': "default msg line 3",
               'line4': "default msg line 4"
               },
       'backlight': 1}

# ################################################################################
# Error Handlers
# ################################################################################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# ################################################################################
# Routes
# ################################################################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lcd/msg')
def lcd_message():

    print(f"Current message is '{ lcd['msg'] }'")
    return render_template('lcd.html', lines=lcd['msg'])


@app.route('/lcd/clear')
def lcd_clear_message():

    lcd['msg'] = {'line1': '', 'line2': '', 'line3': '', 'line4': ''}

    # if request.accept_mimetypes.accept_json and \
    #    not request.accept_mimetypes.accept_html:
    #     return(jsonify({'state': 'display cleared'}))

    return render_template('lcd.html', msg=lcd['msg'])


@app.route('/lcd/set', methods=['GET', 'POST'])
def lcd_set_message():
    form = lcd_set_form(request.form)

    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')

    print(f"Request Methon: {request.method}")
    if request.method == 'POST':
        print(f"  Valid form? {form.validate()}")

        if form.validate():
            print("Processing submitted form data...")
            lcd['msg']['line1'] = form.line1.data
            lcd['msg']['line2'] = form.line2.data
            lcd['msg']['line3'] = form.line3.data
            lcd['msg']['line4'] = form.line4.data

            print("redirecting to GET display resource...")
            return redirect(url_for('lcd_message'))
        else:
            return render_template('lcd_set.html', form=form)

    else:  # was a GET message
        form = lcd_set_form()

        print("Displaying form for user data entry`...")
        form.line1.data = lcd['msg']['line1']
        form.line2.data = lcd['msg']['line2']
        form.line3.data = lcd['msg']['line3']
        form.line4.data = lcd['msg']['line4']
        return render_template('lcd_set.html', form=form)


# ################################################################################
# Startup
# ################################################################################



if __name__ == '__main__':
    # manager.run()
    print(f"Current Servers Host ip: {get_ip_address()}")

    app.run(debug=True)
