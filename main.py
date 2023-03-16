from flask import Flask, render_template, redirect
from flask_login import  LoginManager,login_user, login_required, logout_user
from data.models.users import User
from data.forms import LoginForm, JobForm, RegisterForm
from data import db_session
from uuid import uuid4
app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    print(user_id)
    return db_sess.query(User).get(user_id)





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password_2.data != form.password_1.data:
            return render_template('register.html',
                                   message="пароли не совпадают",
                                   form=form)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   message="Данный email уже есть",
                                   form=form)
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password_1.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('front/html/registration.html', title='Авторизация', form=form)


@app.route('/')
def index():
    form = LoginForm()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('front/html/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('front/html/login.html', title='Авторизация', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    db_session.global_init('db/DataBase.db')
    app.run(debug=True)


if __name__ == '__main__':
    main()
