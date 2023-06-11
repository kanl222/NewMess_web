import flask
from flask import request, abort, jsonify
from sqlalchemy import and_, or_
from flask_login import current_user, login_required
from .. import db_session
from ..__all_models import User, Chat, ChatParticipant, Message, MessagesRead

blueprint = flask.Blueprint(
    'api_search',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/search-users', methods=['GET'])
@login_required
def get_search_users():
    search_value = request.args.get('search_value', '')
    with db_session.create_session() as session:
        users = session.query(User).filter(and_(
            User.username.like('%{}%'.format(search_value)),
            and_(User.id != current_user.get_id(), User.is_admin == 0)
        )).all()
        print(users)
        users_dict = [user.to_dict() for user in users]
        return jsonify({
            "statusCode": 200,
            "message": "The request was successful",
            'data': {
                "users": users_dict
            }
        })


@blueprint.route('/api/search-chats', methods=['GET'])
@login_required
def get_search_chats():
    search_value = request.args.get('search_value', '')
    with db_session.create_session() as session:
        chats_not_private_chat = session.query(Chat).join(
            ChatParticipant, Chat.id == ChatParticipant.chat_id
        ).filter(and_(
            ChatParticipant.user_id == current_user.id,
            Chat.title.like('%{}%'.format(search_value),
                            Chat.is_private_chats == False
                            )
        )).all()
        chats_private_chat = session.query(Chat) \
            .join(ChatParticipant, Chat.id == ChatParticipant.chat_id) \
            .join(User, ChatParticipant.user_id == User.id). \
            filter(ChatParticipant.chat_id.in_(
            session.query(ChatParticipant.chat_id). \
                filter(ChatParticipant.user_id == current_user.id))) \
            .filter(and_(
            User.username.like('%{}%'.format(search_value)),
            Chat.is_private_chats == True
        )).all()

        chats_dict = []
        for chat in chats_not_private_chat:
            last_message = session.query(Message) \
                .filter(Message.chat_id == chat.id) \
                .order_by(Message.send_time.desc()) \
                .first()
            count_new_message = session.query(Message) \
                .outerjoin(MessagesRead,
                           and_(Message.id == MessagesRead.id_message, MessagesRead.id_user == current_user.id)) \
                .filter(MessagesRead.id == None) \
                .filter(Message.chat_id == chat.id) \
                .filter(Message.user_id != current_user.id) \
                .count()

            last_message_text = last_message.text if last_message is not None else ""
            send_time = last_message.date_to_millis() if last_message is not None else ''
            last_message_id = last_message.id if last_message is not None else ""

            chat_dict = {'id': chat.id,
                         'title': chat.title,
                         'icon': chat.icon,
                         'last_message_id': last_message_id,
                         'last_message': last_message_text,
                         'count_new_message': count_new_message,
                         'send_time': send_time}
            chats_dict.append(chat_dict)
        for chat in chats_private_chat:
            last_message = session.query(Message) \
                .filter(Message.chat_id == chat.id) \
                .order_by(Message.send_time.desc()) \
                .first()
            count_new_message = session.query(Message) \
                .outerjoin(MessagesRead,
                           and_(Message.id == MessagesRead.id_message, MessagesRead.id_user == current_user.id)) \
                .filter(MessagesRead.id == None) \
                .filter(Message.chat_id == chat.id) \
                .filter(Message.user_id != current_user.id) \
                .count()
            another_user: User = session.query(User).join(ChatParticipant, ChatParticipant.chat_id == chat.id).filter(
                and_(User.id == ChatParticipant.user_id, ChatParticipant.user_id != current_user.id)).first()
            last_message_text = last_message.text if last_message is not None else ""
            send_time = last_message.date_to_millis() if last_message is not None else ''
            last_message_id = last_message.id if last_message is not None else ""

            chat_dict = {'id': chat.id,
                         'title': another_user.username,
                         'icon': another_user.icon,
                         'last_message_id': last_message_id,
                         'last_message': last_message_text,
                         'count_new_message': count_new_message,
                         'send_time': send_time}
            chats_dict.append(chat_dict)
        return jsonify({
            "statusCode": 200,
            "message": "The request was successful",
            'data': {
                "chats": chats_dict
            }
        })
