import logging
from uuid import uuid4

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from lazy_object_proxy.simple import Proxy


from championship_service.utils.serializer import dumps, loads


logger = logging.getLogger(__name__)


class ChampionshipKafkaProducer(KafkaProducer):
    def __init__(self):
        super().__init__(
            value_serializer=lambda m: dumps(m).encode('utf-8'),
            bootstrap_servers='robot-championship-kafka:9092'
        )

    def send(self, value):
        return super().send('robot-championship.championships', value)


class ChampionshipKafkaConsumer(KafkaConsumer):
    def __init__(self):
        super().__init__(
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers='robot-championship-kafka:9092',
            auto_offset_reset='earliest',
            group_id=str(uuid4()),
        )

        self.my_partition = TopicPartition('robot-championship.championships', 0)
        self.assigned_topic = [self.my_partition]
        self.assign(self.assigned_topic)

    def get_all_events(self):
        events = []
        self.seek_to_beginning(self.my_partition)
        for _ in range(10):
            msg_pack = self.poll(timeout_ms=0.05)
            for tp, messages in msg_pack.items():
                for message in messages:
                    events.append(message.value)
        return events
        
        
championship_message_sender = Proxy(ChampionshipKafkaProducer)


def championship_event_one_time_consumer_factory():
    return ChampionshipKafkaConsumer()


def init_championship_event_listening(app):
    from championship_service.messaging.championship_event_handler import ChampionshipKafkaListener
    logger.info('Initializing message listening')
    championship_event_consumer = ChampionshipKafkaListener(KafkaConsumer(
        'robot-championship.championships',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers='robot-championship-kafka:9092',
        group_id='championship-service'
    ), championship_message_sender, app)
    championship_event_consumer.start()
