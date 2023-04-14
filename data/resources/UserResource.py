from flask import  request,jsonify
from flask_restful import Resource, abort
from ..models.users import User
from .. import db_session
from flask_login import login_required, current_user


def get_or_abort_404(session, model, identifier):
    resource = session.query(model).filter_by(id=identifier).first()
    if not resource:
        abort(404, f"Resource with id {identifier} not found")
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
                abort(400, "Username already exists")
            if 'email' in data and session.query(User).filter(User.email == data['email']).first():
                abort(400, "Email already exists")
            user = User(username=data['username'], email=data['email'])
            session.add(user)
            session.commit()
            return jsonify({"statusCode": 201,
                            "message": "The request was successful"
                            })

    def put(self,user_id=0):
        if not user_id:
            user_id = current_user.id
        with db_session.create_session() as session:
            data = request.json
            if 'username' in data and session.query(User).filter(User.username == data['username']).filter(User.id != user_id).first():
                abort(400, "Username already exists")
            if 'email' in data and session.query(User).filter(User.email == data['email']).filter(User.id != user_id).first():
                abort(400, "Email already exists")
            user = get_or_abort_404(session, User, current_user.id)
            if user != current_user:
                abort(403, "You don't have permission to modify this user")
            print(data)
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
                abort(403, "You don't have permission to delete this user")
            session.delete(user)
            session.commit()
            return jsonify({"statusCode": 204,
                            "message": "The request was successful"}), 204
