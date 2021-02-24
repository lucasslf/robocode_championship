import logging
from uuid import uuid4, UUID

from flask import Blueprint, request, Response, current_app
from werkzeug.exceptions import HTTPException

from championship_service.domain.championship import Championship, ChampionshipEventRepository
from championship_service.infra.kafka import (
    championship_event_one_time_consumer_factory,
    championship_message_sender,
)
from championship_service.utils import serializer

bp = Blueprint('championship', __name__, url_prefix='/championship')

logger = logging.getLogger(__name__)


@bp.route(
    '/',
    methods=['POST']
)
def root():
    data = request.get_json()
   
    try:
        _validate_new_data(data)
        robots = list(map(UUID, data['robots']))
        c = Championship.create(
            championship_id=uuid4(),
            championship_name=data['name'],
            robots=robots,
        )
        repo = ChampionshipEventRepository(
            championship_event_one_time_consumer_factory(),
            championship_message_sender,
        )
        repo.save(c)
        return json_response(c.current_state)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            description=str(e),
            response=Response(
                status=400,
                response=str(e),
            )
        )


@bp.route(
    '/<championship_id>/start',
    methods=['POST']
)
def start_championship(championship_id):

    try:
        repo = ChampionshipEventRepository(
            championship_event_one_time_consumer_factory(),
            championship_message_sender,
        )
        championship = repo.get(championship_id)
        championship.start()
        repo.save(championship)
        return json_response(championship.current_state)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            description=str(e),
            response=Response(
                status=400,
                response=str(e),
            )
        )


@bp.route(
    '/<championship_id>',
    methods=['GET', 'DELETE']
)
def championship_by_id(championship_id):
    repo = ChampionshipEventRepository(
        championship_event_one_time_consumer_factory(),
        championship_message_sender,
    )
    championship = repo.get(championship_id)
    if request.method == 'GET':
        return json_response(championship.current_state)
    if request.method == 'DELETE':
        championship.delete()
        repo.save(championship)


def _validate_new_data(data):
    required_fields = ['name', 'robots']
    errors = []
    for field in required_fields:
        if field not in data:
            logger.info(f'{field} was not passed.')
            errors.append(f'{field} is required.\n')

    if 'robots' in data and len(data['robots']) < 2:
        logger.info('Only one Robot was passed.')
        errors.append('A championship needs at least two robots to start.')

    if errors:
        raise Exception(''.join(errors))


def json_response(data):
    return current_app.response_class(
        serializer.dumps(data) + "\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
