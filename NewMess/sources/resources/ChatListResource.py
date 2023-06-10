from flask import request, jsonify
from flask_restful import Resource,abort
from sqlalchemy import and_
from flask_login import login_required, current_user
from ..models.chat import Chat
from ..models.chat_participants import ChatParticipant
from ..models.chats_read import ChatsRead
from ..models.users import User
from .. import db_session


class ChatListResource(Resource):
    method_decorators = [login_required]

    def get(self):
        args = request.args.to_dict()
        current_user_id = current_user.id
        with db_session.create_session() as db_sess:
            if 'list_chats_id' in args:
                list_chats_id = args['list_chats_id'].split(',')
                chats = db_sess.query(Chat)\
                    .join(ChatParticipant, ChatParticipant.user_id==current_user_id)\
                    .filter(and_(Chat.id == ChatParticipant.chat_id, Chat.id.in_(list_chats_id)))\
                    .all() if len(list_chats_id) > 1 else db_sess.query(Chat)\
                    .join(ChatParticipant, ChatParticipant.user_id==current_user_id)\
                    .filter(and_(Chat.id == ChatParticipant.chat_id, Chat.id == list_chats_id[0]))\
                    .all()
            else:
                chats = db_sess.query(Chat)\
                    .join(ChatParticipant, ChatParticipant.user_id==current_user_id)\
                    .filter(ChatParticipant.chat_id == Chat.id)\
                    .all()
            chats_dict = []
            for chat in chats:
                if chat.is_private_chats:
                    another_user: User = db_sess.query(User)\
                    .join(ChatParticipant, ChatParticipant.chat_id == chat.id)\
                    .filter(and_(User.id == ChatParticipant.user_id,ChatParticipant.user_id != current_user_id))\
                    .first()
                    chat_dict = {
                            'id': chat.id,
                            'title': another_user.username,
                            'icon': another_user.icon
                                }
                                
                    chats_dict.append(chat_dict)
                else:
                    chats_dict.append(chat.to_dict())
            chats_to_add = [ChatsRead(id_user=current_user_id, id_chat=chat.id) for chat in chats
                            if not db_sess.query(ChatsRead).filter_by(id_user=current_user_id, id_chat=chat.id).first()]

            db_sess.add_all(chats_to_add)
            db_sess.commit()

        return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            'chats': chats_dict
                        }})
