from flask import request, jsonify,abort
from flask_restful import Resource
from sqlalchemy import and_
from ..models.messages import Message
from ..models.chat_participants import ChatParticipant
from .. import db_session
from flask_login import login_required, current_user

def get_or_abort_404(session, model, identifier):
    resource = session.query(model).filter_by(id=identifier).first()
    if not resource:
        abort(404, f"Resource with id {identifier} not found")
    return resource

class MessageResource(Resource):
    method_decorators = [login_required]
    
    def get(self, message_id=None):
        if not message_id:
            return abort(404, f"Id not found")
        db_sess = db_session.create_session()
        message = get_or_abort_404(db_sess,Message,message_id)
        message_dict = message.to_dict()
        db_sess.close()
        return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            "message": message_dict
                                 
                        }})
        
    def post(self):
        data = request.json
        db_sess = db_session.create_session()
        chat_user = db_sess.query(ChatParticipant).filter_by(user_id=current_user.id,chat_id = data['chat_id']).first()
        if not chat_user:
            db_sess.close()
            return jsonify({"statusCode": 403,
                            "message": "Current user is not a member of the chat"}), 403
        message = Message(user_id=current_user.id,
                          chat_id=data['chat_id'],
                          text=data['text'])
        db_sess.add(message)
        db_sess.commit()
        message_dict = message.to_dict()
        db_sess.close()
        return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            "message": message_dict
                                 
                        }})

    def put(self, message_id):
        data = request.json
        db_sess = db_session.create_session()
        message = get_or_abort_404(db_sess,Message,message_id)
        if message:
            message.text = data['text']
            message_dict = message.to_dict()
            db_sess.commit()
            db_sess.close
            return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            "message":message_dict 
                        }})
        else:
            db_sess.close()
            return None

    def delete(self, message_id):
        db_sess = db_session.create_session()
        message = get_or_abort_404(db_sess,Message,message_id)
        if message:
            message_dict = message.to_dict()
            db_sess.delete(message)
            db_sess.commit()
            db_sess.close()
            return jsonify({"statusCode": 200,
                        "message": "The request was successful",
                        'data': {
                            "message":message_dict
                        }})
        else:
            return None
