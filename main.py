from flask import Flask, render_template, redirect
from flask_login import  LoginManager,login_user, login_required, logout_user,current_user
from data.models.users import User
from data.forms import LoginForm, RegisterForm
from data.api import api_chat
from data import db_session
from uuid import uuid4
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_session.global_init('db/DataBase.db')



login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(user_id))





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password_2.data != form.password_1.data:
            return render_template('front/register.html',
                                   message="пароли не совпадают",
                                   form=form)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('front/register.html',
                                   message="Данный email уже есть",
                                   form=form)
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password_1.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')

    return render_template('front/register.html', title='Авторизация', form=form)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/mes')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect('/mes')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('front/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('front/login.html', title='Авторизация', form=form)

@app.route('/mes')
def chats_menu():
    if current_user.is_authenticated:
        return render_template('back/chats.html')
    return redirect('/login')

@app.route('/users')
@login_required
def users_menu():
    return render_template('back/users.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    app.register_blueprint(api_chat.blueprint)
    app.run(debug=True,threaded=True)


if __name__ == '__main__':
    main()
