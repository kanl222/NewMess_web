from flask import request, jsonify
from flask_restful import Resource,abort
from sqlalchemy import and_
from ..models.users import User
from .. import db_session
from flask_login import login_required, current_user


class UserListResource(Resource):
    method_decorators = [login_required]
    
    def get(self):
        with db_session.create_session() as session:
            users = session.query(User).filter(User.id != current_user.get_id()).all()
            users_dict = [user.to_dict() for user in users]
            return jsonify({"statusCode": 200,
                            "message": "The request was successful",
                            'data': {
                                "users" :users_dict
                                    
                            }})
