import logging
import threading
from uuid import UUID

from robot_service.data.events import ChampionshipEvent
from robot_service.infra.kafka import championship_message_sender
from robot_service.service import robot

logger = logging.getLogger(__name__)


class ChampionshipKafkaConsumer(threading.Thread):
    daemon = True

    def __init__(self, kafka_consumer, app):
        self._app = app
        logger.info('Starting consumer')
        self._consumer = kafka_consumer
        super(ChampionshipKafkaConsumer, self).__init__()

    def run(self):
        for message in self._consumer:
            message = message.value
            logger.info(f'Championship event received {message}')
            if 'event' in message and message['event'] == 'ChampionshipCreated':
                with self._app.app_context():
                    self._handle_championship_created(message)

    def _handle_championship_created(self, event):
        logger.info(f'Handling championship created')
        if 'championship_id' not in event:
            return
        championship_id = event['championship_id']
        if 'robots' not in event:
            logger.info(f'No Robot list, invalid championship')
            self._invalidate_championship(championship_id)
        else:
            robot_ids = event['robots']
            if len(robot_ids) < 2:
                logger.info(f'Only one Robot in list, invalid championship')
                self._invalidate_championship(championship_id)
            elif robot.check_robots_existence([UUID(robot_id) for robot_id in robot_ids]):
                logger.info(f'Valid championship')
                self._validate_championship(championship_id)
            else:
                logger.info(f'Robots not found')
                self._invalidate_championship(championship_id)

    def _invalidate_championship(self, championship_id):
        championship_message_sender.send(
            ChampionshipEvent.championship_invalidated(championship_id)
        )

    def _validate_championship(self, championship_id):
        championship_message_sender.send(
            ChampionshipEvent.championship_validated(championship_id)
        )
