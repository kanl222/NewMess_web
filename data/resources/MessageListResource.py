from flask_restful import Resource, reqparse
from flask import jsonify,request
from ..models.messages import Message
from ..models.chat_participants import ChatParticipant
from .. import db_session
from flask_login import login_required, current_user

class MessageListResource(Resource):
    method_decorators = [login_required]
    
    def get(self):
        args = request.args
        db_sess = db_session.create_session()
        chat_id = args['chat_id']
        chat_user = db_sess.query(ChatParticipant).filter_by(user_id=current_user.id,chat_id = chat_id).first()
        if not chat_user:
            return jsonify({"statusCode": 403,
                            "message": "Current user is not a member of the chat"}),403
        messages = db_sess.query(Message).filter(Message.chat_id == chat_id).all()
        return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            "messages":[message.to_dict() for message in messages]
                                 
                        }})
