from flask import request, jsonify
from flask_restful import Resource,abort
from sqlalchemy import and_
from flask_login import login_required, current_user
from ..models.chat_participants import ChatParticipant
from ..models.chats_read import ChatsRead
from ..models.users import User
from ..models.chat import Chat
from ..models.messages import Message
from .. import db_session


class ChatParticipantResource(Resource):
    method_decorators = [login_required]

    def get(self):
        with db_session.create_session() as db_sess:
            participants = db_sess.query(ChatParticipant).filter(ChatParticipant.user_id == current_user.id).all()
            res = []
            for participant in participants:
                chat_participant = {
                    'chat_id': participant.chat_id,
                    'user_id': participant.user_id
                }
                res.append(chat_participant)
            return jsonify(res)
    
    def post(self,chat_id=0):
        if request.json.get('chat_id'):
            chat_id = request.json.get('chat_id')
        else:
            chat_id = chat_id
        user_id = current_user.id
        with db_session.create_session() as db_sess:
            participant = ChatParticipant(chat_id=chat_id, user_id=current_user.id)
            db_sess.add(participant)
            db_sess.commit()
            return jsonify({'message': f'Participant {user_id} added to chat {chat_id}.'})
        
    def put(self,chat_id=0):
        if request.json.get('chat_id'):
            chat_id = request.json.get('chat_id')
        else:
            chat_id = chat_id
        user_id = current_user.id
        with db_session.create_session() as db_sess:
            participant = db_sess.query(ChatParticipant).filter(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user_id).first()
            if participant is None:
                return jsonify({'error': f'Participant {user_id} not found in chat {chat_id}.'})
            else:
                participant.is_muted = request.json.get('is_muted', participant.is_muted)
                db_sess.commit()
                return jsonify({'message': f'Participant {user_id} updated in chat {chat_id}.'})
        
    def delete(self,chat_id=0):
        print(chat_id)
        if not chat_id:
            chat_id = request.json.get('chat_id')
        else:
            chat_id = chat_id
        user_id = current_user.id
        with db_session.create_session() as db_sess:
            print(chat_id)
            participant = db_sess.query(ChatParticipant).filter(ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user_id).first()
            users = db_sess.query(User).join(ChatParticipant,ChatParticipant.chat_id==chat_id).filter(and_(ChatParticipant.user_id == User.id, ChatParticipant.user_id != current_user.id)).count()
            if participant is None:
                return jsonify({'error': f'Participant {user_id} not found in chat {chat_id}.'})
            else:
                db_sess.delete(participant)
                if users == 0:
                    db_sess.query(Message).filter(Message.chat_id == chat_id).delete()
                    db_sess.query(Chat).filter(Chat.id == chat_id).delete()
                    db_sess.query(ChatsRead).filter(ChatsRead.id_chat == chat_id).delete()
                db_sess.commit()
                return jsonify({'message': f'Participant {user_id} removed from chat {chat_id}.'})

