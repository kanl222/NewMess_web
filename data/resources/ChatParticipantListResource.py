from flask_restful import Resource, reqparse
from flask import jsonify,request
from ..models.users import User
from ..models.chat_participants import ChatParticipant
from sqlalchemy import and_,or_
from ..support.to_dict import to_dict
from .. import db_session
from flask_login import login_required, current_user

class ChatParticipantListResource(Resource):
    method_decorators = [login_required]
    
    def get(self,chat_id=None):
        args = request.args
        if chat_id is None:    
            chat_id = args['chat_id']
        with db_session.create_session() as db_sess:
            chat_user = db_sess.query(ChatParticipant).filter_by(user_id=current_user.id,chat_id = chat_id).first()
            if not chat_user:
                return jsonify({"statusCode": 403,
                                "message": "Current user is not a member of the chat"}),403
            users = db_sess.query(User.id,User.username,User.icon).join(ChatParticipant,ChatParticipant.chat_id==chat_id).filter(and_(ChatParticipant.user_id == User.id, ChatParticipant.user_id != current_user.id)).all()
            return jsonify({"statusCode": 200,
                            "message": "The request was successful",
                            'data': {
                                "users":[to_dict(['id','username','icon'],users)]
                                    
                            }})
