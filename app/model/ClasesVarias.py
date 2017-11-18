
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, DataRequired


class NameForm(FlaskForm):
    # name = StringField('What is your name?', validators=[Required()])
    id_user = StringField('Introduce tu id_user', validators=[DataRequired()])
    password = StringField('Introduce tu contraseña', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm2(FlaskForm):
    name2 = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
