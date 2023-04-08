from flask import request,jsonify
from flask_restful import Resource
from sqlalchemy.orm import joinedload
from ..models.chats import Chat
from ..models.chat_participants import ChatParticipant
from .. import db_session
from flask_login import login_required, current_user


class ChatListResource(Resource):
    method_decorators = [login_required]
    
    def get(self):
        session = db_session.create_session()
        chats = session.query(Chat).options(joinedload(ChatParticipant)).\
                filter(ChatParticipant.user_id == current_user.id).all()
        session.close()
        chats_dict = [chat.to_dict() for chat in chats]
        return jsonify({"statusCode": 200, "message": "The request was successful",'chats':chats_dict})
