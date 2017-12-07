
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField,\
    IntegerField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, DataRequired


class LoginForm(FlaskForm):
    # name = StringField('What is your name?', validators=[Required()])
    # username = StringField('Introduce tu id_user', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    # submit = SubmitField('Submit')

class IncidenciaForm(FlaskForm):
    titulo = StringField('Titulo de la incidencia', validators=[DataRequired()])
    descripcion_incidencia = TextAreaField('Descripción', validators=[DataRequired()])
    id_dispositivo = StringField('Dispositivo afectado')
    fecha_incidencia = DateField('Fecha de la incidencia', validators=[DataRequired()])
    categoria = SelectField('Categoria' , choices=[('Hardware'), ('Software_básico'),
                                                   ('Problemas con aplicaciones'),
                                                   ('Software de aplicaciones')])



