import logging

from flask import Blueprint, request, Response, current_app
from werkzeug.exceptions import HTTPException

from robot_service.service.robot import (
    add_robot,
    get_robots,
    delete_robot,
    get_robots_by_id,
)
from robot_service.utils import serializer

bp = Blueprint('robots', __name__, url_prefix='/robots')

logger = logging.getLogger(__name__)


@bp.route(
    '/',
    methods=['GET', 'POST']
)
def root():
    if request.method == 'GET':
        return json_response(get_robots())
    if request.method == 'POST':
        data = request.form
        try:
            _validate_new_robot_data(data, request.files)
            return json_response(add_robot(data, request.files['file']))
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                description=str(e),
                response=Response(
                    status=400,
                    response=str(e),
                )
            )


@bp.route(
    '/<robot_id>',
    methods=['GET', 'DELETE']
)
def robot_by_id(robot_id):
    if ',' in robot_id:
        robot_id = list(map(str.strip, robot_id.split(',')))
    if request.method == 'GET':
        robots = get_robots_by_id(robot_id)
        return json_response(robots)

    if request.method == 'DELETE':
        delete_robot(robot_id)
        return current_app.response_class(
            status=204
        )


def _validate_new_robot_data(data, files):
    if not data:
        raise Exception('Robot data is required')

    if 'name' not in data:
        raise Exception('Robot name is required')

    if not files or 'file' not in files:
        raise Exception('Robot jar file is required')


def json_response(data):
    return current_app.response_class(
        serializer.dumps(data) + "\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
