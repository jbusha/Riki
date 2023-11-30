"""
    Forms
    ~~~~~
"""
from flask_wtf import FlaskForm

from wtforms import BooleanField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp
from wtforms.validators import ValidationError

import re

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(FlaskForm):
    url = StringField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(FlaskForm):
    term = StringField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(FlaskForm):
    title = StringField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = StringField('')


class LoginForm(FlaskForm):
    name = StringField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')

class UserSignUp(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [
        InputRequired()])
    confirm_pass = PasswordField('Confirm password', [InputRequired(), EqualTo('password', message='Passwords must match.')])

    def validate_username(form, field):
        user = current_users.get_user(field.data)
        if user:
            raise ValidationError("Username has already been taken.")

    def validate_confirm_pass(form, field):
        confirm_pass = field.data
        if not any(char.isdigit() for char in confirm_pass):
            raise ValidationError("Password must contain at least one digit.")
        if len(confirm_pass) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

