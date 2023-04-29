from flask import request,jsonify,Response
from flask_restful import Resource, abort
from ..models.user import User
from ..models.chat_participants import ChatParticipant
from .. import db_session
from flask_login import login_required, current_user

def get_or_abort_404(session, model, identifier):
    resource = session.query(model).filter_by(id=identifier).first()
    if not resource:
        abort(Response(f"Resource with id {identifier} not found", 404))
    return resource

class UserResource(Resource):
    method_decorators = [login_required]
    
    def get(self, user_id=None):
        with db_session.create_session() as session:
            user = get_or_abort_404(session, User, user_id if user_id else current_user.id )
            user_dict = user.to_dict()
            return jsonify({"statusCode": 201,
                            "message": "The request was successful",
                            'data': {
                                "user": user_dict
                                    
                            }})

    def post(self):
        with db_session.create_session() as session:
            data = request.json
            if 'username' in data and session.query(User).filter(User.username == data['username']).first():
                abort(Response(f"Username already exists", 400))
            if 'email' in data and session.query(User).filter(User.email == data['email']).first():
                abort(Response(f"Email already exists", 400))

            user = User(username=data['username'], email=data['email'])
            session.add(user)
            session.commit()
            return jsonify({"statusCode": 201,
                            "message": "The request was successful"
                            })

    def put(self):
        with db_session.create_session() as session:
            data = request.json
            if 'username' in data and session.query(User).filter(User.username == data['username']).filter(User.id != current_user.id).first():
                 abort(Response(f"Username already exists", 400))
            if 'email' in data and session.query(User).filter(User.email == data['email']).filter(User.id != current_user.id).first():
                abort(Response(f"Email already exists", 400))
            user = get_or_abort_404(session, User, current_user.id)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.icon = data.get('icon', user.icon)
            session.commit()
            return jsonify({"statusCode": 200,
                            "message": "The request was successful"
                            })


    def delete(self, user_id):
        with db_session.create_session() as session:
            user = get_or_abort_404(session, User, user_id)
            if user != current_user:
                abort(Response(f"You don't have permission to delete this user", 403))
            
            records = session.query(ChatParticipant).filter(ChatParticipant.user_id == user.id).all()
            
            for record in records:
                session.delete(record)
                
            session.delete(user)
            session.commit()

            return jsonify({"statusCode": 204,
                            "message": "The request was successful"})
