from flask import render_template, redirect, Blueprint, request
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import and_
from ..models.users import User
from ..models.chat import Chat
from ..models.chats_read import ChatsRead
from ..models.chat_participants import ChatParticipant
from ..models.messages import Message
from ..models.messages_read import MessagesRead
from ..forms import LoginForm, RegisterForm
from ..support.create_avatar import generate_avatar
from .. import db_session

path_base = 'front/base.html'

blueprint = Blueprint(
    'routes',
    __name__,
    template_folder='templates'
)


@blueprint.route('/mes')
def chats_menu():
    if not current_user.is_authenticated:
        return redirect('/login')  #
    current_user_id = current_user.id
    with db_session.create_session() as db_sess:
        chats = db_sess.query(Chat) \
            .join(ChatParticipant, Chat.id == ChatParticipant.chat_id) \
            .filter(ChatParticipant.user_id == current_user.id) \
            .all()
        chats_ = []
        for chat_ in chats:
            if not chat_.is_private_chats:
                latest_message = db_sess.query(Message.id, Message.text, Message.send_time) \
                    .filter(Message.chat_id == chat_.id) \
                    .order_by(Message.send_time.desc()) \
                    .first()
                count_new_message = db_sess.query(Message) \
                    .outerjoin(MessagesRead,
                               and_(Message.id == MessagesRead.id_message, MessagesRead.id_user == current_user_id)) \
                    .filter(MessagesRead.id == None) \
                    .filter(Message.chat_id == chat_.id) \
                    .filter(Message.user_id != current_user_id) \
                    .count()
                latest_message_text = latest_message[1] if latest_message is not None else ""
                send_time = latest_message[2].strftime("%H:%M") if latest_message is not None else ''
                latest_message_id = latest_message[0] if latest_message is not None else ""

                chat_dict = {'id': chat_.id,
                             'title': chat_.title,
                             'icon': chat_.icon,
                             'last_message_id': latest_message_id,
                             'last_message': latest_message_text,
                             'count_new_message': count_new_message,
                             'send_time': send_time}
                chats_.append(chat_dict)
            elif chat_.is_private_chats:
                last_message = db_sess.query(Message.id, Message.text, Message.send_time) \
                    .filter(Message.chat_id == chat_.id) \
                    .order_by(Message.send_time.desc()) \
                    .first()
                count_new_message = db_sess.query(Message) \
                    .outerjoin(MessagesRead,
                               and_(Message.id == MessagesRead.id_message, MessagesRead.id_user == current_user_id)) \
                    .filter(MessagesRead.id == None) \
                    .filter(Message.chat_id == chat_.id) \
                    .filter(Message.user_id != current_user_id) \
                    .count()
                another_user: User = db_sess.query(User) \
                    .join(ChatParticipant, ChatParticipant.chat_id == chat_.id) \
                    .filter(and_(User.id == ChatParticipant.user_id, ChatParticipant.user_id != current_user_id)) \
                    .first()
                last_message_text = last_message[1] if last_message is not None else ""
                send_time = last_message[2].strftime("%H:%M") if last_message is not None else ''
                last_message_id = last_message[0] if last_message is not None else ""

                chat_dict = {'id': chat_.id,
                             'title': another_user.username,
                             'icon': another_user.icon,
                             'last_message_id': last_message_id,
                             'last_message': last_message_text,
                             'count_new_message': count_new_message,
                             'send_time': send_time}
                chats_.append(chat_dict)
        chats_to_add = []
        for chat in chats:
            if not db_sess.query(ChatsRead).filter_by(id_user=current_user_id, id_chat=chat.id).first():
                chats_to_add.append(ChatsRead(id_user=current_user_id, id_chat=chat.id))
                db_sess.add_all(chats_to_add)
                db_sess.commit()

    if request.args.get('chat_id', 0):
        return render_template('back/user/chats.html', title='Мессенджер', chats=chats_,
                               open_chat_id=request.args.get('chat_id'))
    else:
        return render_template('back/user/chats.html', title='Мессенджер', chats=chats_)


@blueprint.route('/users')
def users_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    with db_session.create_session() as db_sess:
        users = db_sess.query(User).filter(and_(User.id != current_user.get_id(), User.is_admin == 0)).all()
        return render_template('back/user/users.html', users=users, title='Пользователи')


@blueprint.route('/sittings')
def sittings_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('back/user/sittings.html', title='Настройки')


@blueprint.route('/admin/users')
def admin_users_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    if not current_user.is_admin:
        return redirect('/login')
    with db_session.create_session() as db_sess:
        users = db_sess.query(User).filter(User.id != current_user.get_id()).all()
        return render_template('back/admin/users.html', title='Пользователи', users=users)


@blueprint.route('/admin/chats')
def admin_chats_menu():
    if not current_user.is_authenticated:
        return redirect('/login')
    if not current_user.is_admin:
        return redirect('/login')
    with db_session.create_session() as db_sess:
        chats = db_sess.query(Chat).all()
        return render_template('back/admin/chats.html', title='Чаты', chats=chats)
