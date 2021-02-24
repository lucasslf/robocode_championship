import logging
import threading

from championship_service.data.events import ChampionshipEvent, BattleEvent

logger = logging.getLogger(__name__)


class ChampionshipKafkaListener(threading.Thread):
    daemon = True

    def __init__(self, kafka_consumer, kafka_producer, app):
        self._app = app
        logger.info('Starting consumer')
        self._consumer = kafka_consumer
        self._producer = kafka_producer
        super(ChampionshipKafkaListener, self).__init__()

    def run(self):
        for message in self._consumer:
            message = message.value
            logger.info(f'Championship event received {message}')
            event = ChampionshipEvent.decode(message)
            with self._app.app_context():
                self._handle_event(event)
    
    def _handle_event(self, event: ChampionshipEvent):
        logger.info(f'Handling {event}')
        if 'ChampionshipStarted' == event.event:
            pairs = _get_pairings(event.robots)
            for pair in pairs:
                battle_created = BattleEvent.battle_created(
                    championship_id=event.championship_id,
                    robot_1=pair[0],
                    robot_2=pair[1],
                )
                self._producer.send(battle_created)


def _get_pairings(robots):
    pairs = []
    robot_count = len(robots)
    for i in range(robot_count):
        for j in range(i + 1, robot_count):
            pairs.append((robots[i], robots[j]))
    return pairs
