from flask import Flask, render_template, redirect
from flask_login import  LoginManager,login_user, login_required, logout_user,current_user
from flask_restful import Resource, Api, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import and_,or_
from sqlalchemy.sql.expression import func
from data.models.users import User
from data.models.chats import Chat
from data.models.chats_read import chats_read
from data.models.chat_participants import ChatParticipant
from data.models.messages import Message
from data.forms import LoginForm, RegisterForm
from data.resources import ChatListResource, ChatResorce, UserListResource,UserResource,MessageListResource,MessageResource
from data.support.create_avatar import generate_avatar
from data.api import api_chat
from data.api import api_support
from data import db_session
from uuid import uuid4
import ssl
import os

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
app.config['SECRET_KEY'] = uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_session.global_init('db/DataBase.db')


login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,int(user_id))


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
        user.icon = generate_avatar(form.username.data,return_PNG_bytes=True)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')

    return render_template('front/register.html', title='Авторизация', form=form)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    return redirect('/mes')

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
    if not current_user.is_authenticated:
        return redirect('/login')
    current_user_id = current_user.id
    db_sess = db_session.create_session()
    chats = db_sess.query(Chat).join(ChatParticipant,Chat.id == ChatParticipant.chat_id).filter(ChatParticipant.user_id == current_user.id).all()
    chats_to_add = []
    print(chats)
    for chat in chats:
        if not db_sess.query(chats_read).filter_by(id_user=current_user_id, id_chat=chat.id).first():
            chats_to_add.append(chats_read(id_user=current_user_id, id_chat=chat.id))

    db_sess.add_all(chats_to_add)
    return render_template('back/chats.html',title='Мессенджер',chats=chats)

@app.route('/users')
def users_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id != current_user.get_id()).all()
    db_sess.close()
    return render_template('back/users.html',users=users)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def register_blueprint():
    app.register_blueprint(api_chat.blueprint)
    app.register_blueprint(api_support.blueprint)

def register_api():
    api.add_resource(ChatResorce.ChatResource, '/api/chat', '/api/chat/<int:chat_id>')
    api.add_resource(ChatListResource.ChatListResource, '/api/chats')
    api.add_resource(UserResource.UserResource, '/api/user', '/api/user/<int:user_id>')
    api.add_resource(UserListResource.UserListResource, '/api/users')
    api.add_resource(MessageResource.MessageResource, '/api/message', '/api/message/<int:user_id>')
    api.add_resource(MessageListResource.MessageListResource, '/api/messages')

    
def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('example.crt', 'example.key')
    register_blueprint()
    register_api()
    app.run(host='127.0.0.1',debug=True,threaded=True)


if __name__ == '__main__':
    main()
