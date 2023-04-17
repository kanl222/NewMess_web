from flask import Flask, render_template, redirect,jsonify
from flask_login import  LoginManager,login_user, login_required, logout_user,current_user
from flask_restful import Api, abort
from sqlalchemy import and_
from data.models.users import User
from data.models.chats import Chat
from data.models.chats_read import ChatsRead
from data.models.chat_participants import ChatParticipant
from data.models.messages import Message
from data.models.messages_read import MessagesRead
from data.forms import LoginForm, RegisterForm
from data.resources import ChatListResource, ChatResorce, UserListResource,UserResource,MessageListResource,MessageResource,ChatParticipantListResource
from data.support.create_avatar import generate_avatar
from data.api import api_chat
from data.api import api_support
from data.api import api_search
from data import db_session
from uuid import uuid4
import ssl
import time
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v2', action='store_true', help='Enable v2')
parser.add_argument('--ssl-certifacet', action='store_true', help='Path to SSL certificate')

args = parser.parse_args()

if args.v2:
    path_base = 'front/v2-base.html'
else:
    path_base = 'front/base.html'

print(f'SSL certificate path: {args.ssl_certifacet}')



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
    with db_session.create_session() as db_sess:
        return db_sess.get(User,int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
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
            return redirect('/login')

    return render_template('front/register.html', title='Регистрация', form=form, path_base=path_base)


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
        with db_session.create_session() as db_sess:
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('front/login.html',
                                message="Неправильный логин или пароль",
                                form=form)
    return render_template('front/login.html', title='Авторизация', form=form, path_base=path_base)

@app.route('/mes')
def chats_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    current_user_id = current_user.id
    with db_session.create_session() as db_sess:
        chats = db_sess.query(Chat.id, Chat.title, Chat.icon)\
                    .join(ChatParticipant, Chat.id == ChatParticipant.chat_id)\
                    .filter(ChatParticipant.user_id == current_user.id).all()
        chats_ = []
        for chat_ in chats:
            latest_message = db_sess.query(Message.id, Message.text, Message.send_time) \
                                    .filter(Message.chat_id == chat_[0]) \
                                    .order_by(Message.send_time.desc()) \
                                    .first()
            count_new_message = db_sess.query(Message) \
                        .outerjoin(MessagesRead, and_(Message.id == MessagesRead.id_message,MessagesRead.id_user == current_user.id)) \
                        .filter(MessagesRead.id == None) \
                        .filter(Message.chat_id == chat_[0]) \
                        .filter(Message.user_id != current_user.id) \
                        .count()
            latest_message_text = latest_message[1] if latest_message is not None else ""
            send_time = latest_message[2].strftime("%H:%M") if latest_message is not None else ''
            latest_message_id = latest_message[0] if latest_message is not None else ""

            chat_dict = {'id': chat_[0],
                        'title': chat_[1],
                        'icon': chat_[2],
                        'last_message_id': latest_message_id,
                        'last_message': latest_message_text,
                        'count_new_message':count_new_message,
                        'send_time': send_time}
            chats_.append(chat_dict)
        chats_to_add = []
        for chat in chats:
            if not db_sess.query(ChatsRead).filter_by(id_user=current_user_id, id_chat=chat[0]).first():
                chats_to_add.append(ChatsRead(id_user=current_user_id, id_chat=chat[0]))
        db_sess.add_all(chats_to_add)
        db_sess.commit()
    return render_template('back/chats.html',title='Мессенджер',chats=chats_)

@app.route('/users')
def users_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    with db_session.create_session() as db_sess:
        users = db_sess.query(User).filter(User.id != current_user.get_id()).all()
        return render_template('back/users.html',users=users,title='Пользователи')
    
@app.route('/sittings')
def sittings_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('back/sittings.html',title='Настройки')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def register_blueprint():
    app.register_blueprint(api_chat.blueprint)
    app.register_blueprint(api_support.blueprint)
    app.register_blueprint(api_search.blueprint)

def register_api():
    api.add_resource(ChatResorce.ChatResource, '/api/chat', '/api/chat/<int:chat_id>')
    api.add_resource(ChatListResource.ChatListResource, '/api/chats')
    api.add_resource(UserResource.UserResource, '/api/user', '/api/user/<int:user_id>')
    api.add_resource(UserListResource.UserListResource, '/api/users')
    api.add_resource(MessageResource.MessageResource, '/api/message', '/api/message/<int:user_id>')
    api.add_resource(MessageListResource.MessageListResource, '/api/messages')
    api.add_resource(ChatParticipantListResource.ChatParticipantListResource, '/api/chatparticipant', '/api/chatparticipant/<int:chat_id>')

    
def main():
    register_blueprint()
    register_api()
    if args.ssl_certifacet:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain('example.crt', 'example.key')
        app.run(debug=True,threaded=True,ssl_context=context)
    else:
        app.run(debug=True,threaded=True)


if __name__ == '__main__':
    main()
