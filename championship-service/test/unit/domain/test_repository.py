from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4


from championship_service.domain.championship import ChampionshipEventRepository
from championship_service.infra.kafka import ChampionshipKafkaProducer, ChampionshipKafkaConsumer


class TestChampionshipRepository(TestCase):
    
    def setUp(self) -> None:
        self.mock_kafka_consumer = MagicMock(spec=ChampionshipKafkaConsumer)
        self.mock_kafka_producer = MagicMock(spec=ChampionshipKafkaProducer)

    def test_repository_get_championship_pending(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 1
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'pending'
        assert c.current_state.robots == robots

    def test_repository_get_championship_ready(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipValidated'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 2
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'ready'
        assert c.current_state.robots == robots

    def test_repository_get_championship_invalid(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipInvalidated'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 2
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'invalid'
        assert c.current_state.robots == robots

    def test_repository_get_championship_deleted(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipInvalidated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipDeleted'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'deleted'
        assert c.current_state.robots == robots

    def test_repository_get_championship_started(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipValidated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipStarted'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'started'
        assert c.current_state.robots == robots

    def test_repository_get_championship_finished(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipValidated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipStarted'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipFinished'
            },
        ]

        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, None)

        c = repo.get(championship_id)

        assert len(c.events) == 4
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'finished'
        assert c.current_state.robots == robots

    def test_save_flushes_only_new_events(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        events = [
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'championship_name': name,
                'robots': [str(r) for r in robots],
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipCreated'
            },
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipValidated'
            },
        ]
        self.mock_kafka_consumer.get_all_events.return_value = events

        repo = ChampionshipEventRepository(self.mock_kafka_consumer, self.mock_kafka_producer)

        c = repo.get(championship_id)
        c.start()
        repo.save(c)

        self.mock_kafka_producer.send.assert_called_once_with(c.events[2])
