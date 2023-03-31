import flask
from flask import request,abort
import datetime
from flask_login import current_user
from .. import db_session
from ..__all_models import User,Chat

blueprint = flask.Blueprint(
    'api_chat',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_update():
    return flask.jsonify({'jobs': ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date','is_finished']})


@blueprint.route('/api/messages')
def get_messages_in_chat():
    if not current_user.is_authenticated:
        abort(404)
    return flask.jsonify({'jobs': ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date','is_finished']})
