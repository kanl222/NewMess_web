from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit_login = SubmitField('Войти')


class JobForm(FlaskForm):
    job_title = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Начальник работы', validators=[DataRequired()])
    work_size = StringField('Продолжительность работы', validators=[DataRequired()])
    collaborators = StringField('Учаcтники', validators=[DataRequired()])
    is_finished = BooleanField('Работа Закончена')
    submit = SubmitField('Создать')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Ваша должность', validators=[DataRequired()])
    speciality = StringField('Ваша специальность', validators=[DataRequired()])
    address = StringField('Ваш адрес', validators=[DataRequired()])
    email = EmailField('Ваша почта', validators=[DataRequired()])
    password_1 = PasswordField('Пароль', validators=[DataRequired()])
    password_2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


