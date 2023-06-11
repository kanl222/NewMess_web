from flask import Flask, render_template, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import and_
from sources.models.users import User
from sources.forms import LoginForm, RegisterForm
from sources.support.create_avatar import generate_avatar
from sources.api import api_chat, api_search, api_support
from sources.routes import routes
from sources import db_session
from uuid import uuid4
import ssl
import os
from flask import send_from_directory

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
        return db_sess.get(User, int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            if form.password_2.data != form.password_1.data:
                return render_template('front/register.html',
                                       message="пароли не совпадают",
                                       form=form,
                                       path_base=path_base)
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('front/register.html',
                                       message="Данный email уже есть",
                                       form=form,
                                       path_base=path_base)
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password_1.data)
            user.icon = generate_avatar(form.username.data, return_PNG_bytes=True)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')

    return render_template('front/register.html', title='Регистрация', form=form, path_base=path_base)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    if current_user.is_admin:
        return redirect('/admin/users')
    return redirect('/mes')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/back/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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
                                   form=form,
                                   path_base=path_base)
    return render_template('front/login.html', title='Авторизация', form=form, path_base=path_base)


def register_blueprint():
    app.register_blueprint(routes.blueprint)
    app.register_blueprint(api_chat.blueprint)
    app.register_blueprint(api_support.blueprint)
    app.register_blueprint(api_search.blueprint)


def register_api():
    from flask_restful import Api
    from sources.resources import ChatListResource, ChatResorce, UserListResource, UserResource, MessageListResource, \
        MessageResource, ChatParticipantListResource, ChatParticipantResource

    api = Api(app)
    api.add_resource(ChatResorce.ChatResource, '/api/chat', '/api/chat/<int:chat_id>')
    api.add_resource(ChatListResource.ChatListResource, '/api/chats')
    api.add_resource(UserResource.UserResource, '/api/user', '/api/user/<int:user_id>')
    api.add_resource(UserListResource.UserListResource, '/api/users')
    api.add_resource(MessageResource.MessageResource, '/api/message', '/api/message/<int:user_id>')
    api.add_resource(MessageListResource.MessageListResource, '/api/messages')
    api.add_resource(ChatParticipantListResource.ChatParticipantListResource, '/api/chatparticipants/<int:chat_id>')
    api.add_resource(ChatParticipantResource.ChatParticipantResource, '/api/chatparticipant',
                     '/api/chatparticipant/<int:chat_id>')


def main():
    register_blueprint()
    register_api()
    if args.ssl_certifacet:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain('example.crt', 'example.key')
        app.run(debug=True, threaded=True, ssl_context=context)
    else:
        app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
