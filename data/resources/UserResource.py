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
        if not user_id:
            abort(404, f"Id not found")
        session = db_session.create_session()
        user = get_or_abort_404(session, User, user_id)
        session.close()
        return user.to_dict(), 201

    def post(self):
        session = db_session.create_session()
        user = User(username=request.json['username'], email=request.json['email'])
        session.add(user)
        session.commit()
        session.close()
        return user.to_dict(), 201

    def put(self, user_id):
        session = db_session.create_session()
        user = get_or_abort_404(session, User, user_id)
        if user != current_user:
            abort(403, "You don't have permission to modify this user")
        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        session.commit()
        session.close()
        return user.to_dict(), 201

    def delete(self, user_id):
        session = db_session.create_session()
        user = get_or_abort_404(session, User, user_id)
        if user != current_user:
            abort(403, "You don't have permission to delete this user")
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({"statusCode": 204,
                        "message": "The request was successful"}), 204
