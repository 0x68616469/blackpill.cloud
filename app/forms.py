from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField

from .extensions import settings
from .models import User, Nip, Lnaddr

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=70), EqualTo('password_conf', message='Passwords must match')], render_kw={"placeholder": "Password"})
    password_conf = PasswordField("Password confirmation", validators=[InputRequired(), Length(min=1, max=70)], render_kw={"placeholder": "Password Confirmation"})

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=7, max=70)], render_kw={"placeholder": "Password"})

class NipForm(FlaskForm):
    username = StringField("NIP-05 Username", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "username"})
    hex = StringField("Hex Key", validators=[InputRequired(), Length(min=4, max=550)], render_kw={"placeholder": "hex public key"})

    def validate_nip(self, username):
        existing_nip_username = Nip.query.filter_by(username=username.data).first()
        if existing_nip_username:
            raise ValidationError("That NIP-05 username already exists. Please choose a different one.")

class LnaddrForwardForm(FlaskForm):
    username = StringField("Ln Address username", validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "username"})
    forward_to = StringField("Forward to", validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "your lightning address"})

    def validate_lnaddr_in(self, username):
        existing_lnaddr_username = Lnaddr.query.filter_by(username=username.data).first()
        if existing_lnaddr_username:
            raise ValidationError("That username for Lightning Address forwarding already exists. Please choose a different one.")

class MediaForm(FlaskForm):
    image = FileField("Image", validators=[FileRequired(), FileAllowed(settings["allowed_extensions"])])