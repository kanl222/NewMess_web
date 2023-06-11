from flask_restful import Resource, reqparse
from flask import jsonify, request, Response
from flask_restful import abort
from ..models.messages import Message
from ..models.chat_participants import ChatParticipant
from ..models.messages_read import MessagesRead
from .. import db_session
from flask_login import login_required, current_user


class MessageListResource(Resource):
    method_decorators = [login_required]

    def get(self):
        args = request.args
        chat_id = args['chat_id']
        with db_session.create_session() as db_sess:
            chat_user = db_sess.query(ChatParticipant).filter_by(user_id=current_user.id, chat_id=chat_id).first()
            if not chat_user:
                abort(Response(f"Current user is not a member of the chat", 403))
            messages = db_sess.query(Message).filter_by(chat_id=chat_id).all()
            messages_to_add = [MessagesRead(id_user=current_user.id, id_message=message.id)
                               for message in messages
                               if not db_sess.query(MessagesRead).filter_by(id_user=current_user.id,
                                                                            id_message=message.id).first()]
            db_sess.add_all(messages_to_add)
            message_dicts = [message.to_dict() for message in messages]
            db_sess.commit()
            return jsonify({"statusCode": 200,
                            "message": "The request was successful",
                            'data': {
                                "messages": message_dicts
                            }})
