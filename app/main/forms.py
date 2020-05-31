# from flask import Flask, render_template, request, jsonify, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required, length

# ################################################################################
# Form Definitions
# ################################################################################


class lcd_set_form(FlaskForm):
    line1 = StringField('Line1', validators=[length(max=20)])
    line2 = StringField('Line2', validators=[length(max=20)])
    line3 = StringField('Line3', validators=[length(max=20)])
    line4 = StringField('Line4', validators=[length(max=20)])
    submit = SubmitField('submit')
