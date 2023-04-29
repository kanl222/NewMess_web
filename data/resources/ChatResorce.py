from flask import Flask, request,jsonify,Response
from functools import wraps
from sqlalchemy import and_
from flask_restful import abort
from flask_restful import Resource, abort
from ..models.chat import Chat
from ..models.user import User
from ..models.chat_participants import ChatParticipant
from ..models.messages import Message
from ..support.create_avatar import generate_avatar
from .. import db_session
from flask_login import login_required, current_user

def get_or_abort_404(session, model, identifier):
    resource = session.query(model).filter_by(id=identifier).first()
    if not resource:
        abort(Response(f"Resource with id {identifier} not found", 404))
    return resource

def admin_chat_required(session,chat_id):
    chat = session.get(Chat,int(chat_id))
    if chat.admin_chat != current_user.id:
        abort(Response(f"You need to be an admin of this chat to perform this action", 403))

        
class ChatResource(Resource):
    method_decorators = [login_required]
    
    def get(self, chat_id=None):
        if not chat_id:
            abort(404)
        with db_session.create_session() as db_sess:
            chat:Chat = get_or_abort_404(db_sess,Chat,chat_id)
            user_participant = db_sess.query(ChatParticipant).filter_by(chat_id=chat_id).count()
            if not db_sess.query(ChatParticipant).filter_by(chat_id=chat_id, user_id=current_user.id).first():
                abort(Response(f"You don't have permission to modify this chat", 403))
            if chat.is_private_chats:
                another_user: User = db_sess.query(User).join(ChatParticipant,ChatParticipant.chat_id == chat.id).filter(and_(User.id == ChatParticipant.user_id,ChatParticipant.user_id != current_user.id)).first()
                chat.title = another_user.username
                chat.icon = another_user.icon
                return chat.to_dict()
            chat = chat.to_dict()
            chat['user_participant'] = user_participant
            return chat

    def post(self):
        data = request.json
        icon = data.get('icon_base64','')
        list_user_in_chat = data.get('list_user_in_chat', '').split(',')
        with db_session.create_session() as session:
            if 'title' in data and session.query(Chat).filter(Chat.title == data['title']).first():
                abort(Response(f"Title already exists", 400))
            if icon: 
                chat = Chat(title=data['title'], icon=icon,admin_chat=current_user.id)
            elif len(list_user_in_chat) == 1:
                chat = Chat(is_private_chats=True)
            else:
                chat = Chat(title=data['title'], icon=generate_avatar(data['title'], return_PNG_bytes=True),admin_chat=current_user.id)
                    
            session.add(chat)
            session.commit()
            session.refresh(chat)
            list_user_in_chat.append(str(current_user.id))
            
            for user_id in list_user_in_chat:
                chat_participant = ChatParticipant(chat_id=chat.id, user_id=user_id)
                session.add(chat_participant)

            session.commit()
            session.close()
            return jsonify({"statusCode": 200, "message": "The request was successful"})

    def put(self, chat_id):
        with db_session.create_session() as session:
            admin_chat_required(session,chat_id)
            chat = get_or_abort_404(session,Chat,chat_id)
            if chat.user_id != current_user.id:
                abort(Response(f"You don't have permission to modify this chat", 403))
            chat.title = request.json.get('title', chat.title)
            chat.icon = request.json.get('icon', chat.icon)
            session.commit()
            session.close()
            return jsonify({"statusCode": 200, "message": "The request was successful"})


    def delete(self, chat_id):
        with db_session.create_session() as session:
            admin_chat_required(session,chat_id)
            chat = get_or_abort_404(session,Chat,chat_id)
            if chat.user_id != current_user.id:
                abort(403, "You don't have permission to delete this chat")
            session.query(ChatParticipant).filter(ChatParticipant.chat_id == chat.id).delete()
            session.query(Message).filter(Message.chat_id == chat.id).delete()
            session.delete(chat)
            session.commit()
            
            return jsonify({"statusCode": 204, "message": "The request was successful"})
