from flask import request, jsonify, Response
from flask_restful import Resource, abort
from sqlalchemy import and_
from ..models.messages import Message
from ..models.chat_participants import ChatParticipant
from ..models.messages_read import MessagesRead
from .. import db_session
from flask_login import login_required, current_user


def get_or_abort_404(session, model, identifier):
    resource = session.query(model).filter_by(id=identifier).first()
    if not resource:
        abort(Response(f"Resource with id {identifier} not found", 404))
    return resource


class MessageResource(Resource):
    method_decorators = [login_required]

    def get(self, message_id=None):
        if not message_id:
            return abort(404, f"Id not found")
        with db_session.create_session() as db_sess:
            message = get_or_abort_404(db_sess, Message, message_id)
            message_dict = message.to_dict()
            return jsonify({"statusCode": 200,
                            "message": "The request was successful",
                            'data': {
                                "message": message_dict

                            }})

    def post(self):
        data = request.json
        with db_session.create_session() as db_sess:
            chat_user = db_sess.query(ChatParticipant).filter_by(user_id=current_user.id,
                                                                 chat_id=data['chat_id']).first()
            if not chat_user:
                abort(Response(f"Current user is not a member of the chat", 403))
            message = Message(user_id=current_user.id,
                              chat_id=data['chat_id'],
                              text=data['text'])
            db_sess.add(message)
            messages_to_add = MessagesRead(id_user=current_user.id, id_message=message.id)
            db_sess.add(messages_to_add)
            db_sess.commit()
            message_dict = message.to_dict()
            return jsonify({"statusCode": 200,
                            "message": "The request was successful",
                            'data': {
                                "message": message_dict

                            }})

    def put(self, message_id):
        data = request.json
        with db_session.create_session() as db_sess:
            message = get_or_abort_404(db_sess, Message, message_id)
            if message:
                message.text = data['text']
                message_dict = message.to_dict()
                db_sess.commit()
                return jsonify({"statusCode": 200,
                                "message": "The request was successful",
                                'data': {
                                    "message": message_dict
                                }})
            else:
                return None

    def delete(self, message_id):
        with db_session.create_session() as db_sess:
            message = get_or_abort_404(db_sess, Message, message_id)
            if message:
                message_dict = message.to_dict()
                db_sess.delete(message)
                db_sess.commit()
                return jsonify({"statusCode": 200,
                                "message": "The request was successful",
                                'data': {
                                    "message": message_dict
                                }})
            else:
                return None
