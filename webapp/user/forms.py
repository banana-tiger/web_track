from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': "btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    password1 = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password1')],
                              render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': "btn btn-primary"})

    def validate_username(self, username):
        user_exists = User.query.filter_by(username=username.data).count()
        if user_exists > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        email_exists = User.query.filter_by(email=email.data).count()
        if email_exists > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже существует')


