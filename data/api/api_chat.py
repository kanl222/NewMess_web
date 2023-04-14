import flask
from flask import request,abort,jsonify
from sqlalchemy import and_,or_
import json
import datetime
from flask_login import current_user,login_required
from .. import db_session
from ..__all_models import User,Chat,ChatParticipant,Message,MessagesRead,ChatsRead

blueprint = flask.Blueprint(
    'api_chat',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/update')
@login_required
def get_update():
    current_user_id = current_user.id
    with db_session.create_session() as db_sess:
        chats = db_sess.query(Chat.id)\
            .join(ChatParticipant, Chat.id == ChatParticipant.chat_id)\
            .filter(ChatParticipant.user_id == current_user_id)\
            .all()
        
        chats_ = {}
        chats_last_messages = {}
        for chat in chats:
            count_new_message = db_sess.query(Message.id)\
                .outerjoin(MessagesRead, 
                           and_(Message.id == MessagesRead.id_message,
                                MessagesRead.id_user == current_user_id))\
                .filter(MessagesRead.id.is_(None))\
                .filter(Message.chat_id == chat.id)\
                .filter(Message.user_id != current_user_id)\
                .count()
            chats_[chat.id] = count_new_message
            if count_new_message:
                latest_message = db_sess.query(Message) \
                                    .filter(Message.chat_id == chat.id) \
                                    .order_by(Message.send_time.desc()) \
                                    .first()
                                    
                chats_last_messages[chat.id] = latest_message.to_dict()
                                    


        list_unread_chat = db_sess.query(ChatParticipant.chat_id)\
            .outerjoin(ChatsRead, 
                       and_(ChatsRead.id_user == ChatParticipant.user_id,
                            ChatsRead.id_chat == ChatParticipant.chat_id))\
            .filter(ChatsRead.id.is_(None))\
            .filter(ChatParticipant.user_id == current_user_id)\
            .all()


        list_unread_chat = [chat_id for chat_id, in list_unread_chat]

        
        return jsonify({
            "statusCode": 200,
            "message": "The request was successful",
            'data': {
                "list_unread_chat": list_unread_chat,
                'chats_last_messages':chats_last_messages,
                "count_new_messages": chats_
            }
        })


@blueprint.route('/api/new_massage/<int:chat_id>')
@login_required
def get_new_massage(chat_id):
    current_user_id = current_user.id
    with db_session.create_session() as db_sess:
        new_message = db_sess.query(Message) \
                        .outerjoin(MessagesRead, and_(Message.id == MessagesRead.id_message,MessagesRead.id_user == current_user_id)) \
                        .filter(MessagesRead.id == None) \
                        .filter(Message.chat_id == chat_id) \
                        .filter(Message.user_id != current_user_id) \
                        .order_by(Message.id.asc()) \
                        .all()
        messages_to_add = [MessagesRead(id_user=current_user_id, id_message=message.id)
                            for message in new_message
                            if not db_sess.query(MessagesRead).filter_by(id_user=current_user_id, id_message=message.id).first()]
        db_sess.add_all(messages_to_add)
        db_sess.commit()
        new_message = [new_message_.to_dict() for new_message_ in new_message]
        return jsonify({
            "statusCode": 200,
            "message": "The request was successful",
            'data': {
                "new_message": new_message
            }
        })
