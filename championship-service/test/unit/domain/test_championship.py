from datetime import datetime
from unittest import TestCase
from uuid import uuid4

from championship_service.data.events import ChampionshipEvent
from championship_service.domain.championship import Championship


class TestChampionshipDomain(TestCase):

    def test_create_championship(self):
        championship_id = uuid4()
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        name = 'Roborumble'
        c = Championship.create(championship_id, name, robots)
        assert len(c.events) == 1
        assert c.events[0].event == 'ChampionshipCreated'
        assert c.events[0].robots == robots
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'pending'

    def test_domain_event_started(self):
        championship_id = uuid4()
        name = 'Roborumble'
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        event_list = [
            ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots),
            ChampionshipEvent.decode(
                {
                    'id': str(uuid4()),
                    'championship_id': str(championship_id),
                    'created_at': datetime.utcnow().isoformat(),
                    'event': 'ChampionshipValidated'
                }
            ),
            ChampionshipEvent.championship_started(championship_id),
        ]

        c = Championship(championship_id)
        for e in event_list:
            c.add_event(e)

        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'started'
        assert c.current_state.robots == robots

    def test_workflow(self):
        championship_id = uuid4()
        name = 'Roborumble'
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        c = Championship(championship_id)

        c.add_event(ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots))
        assert len(c.events) == 1
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'pending'
        assert c.current_state.robots == robots

        c.add_event(ChampionshipEvent.decode(
            {
                'id': str(uuid4()),
                'championship_id': str(championship_id),
                'created_at': datetime.utcnow().isoformat(),
                'event': 'ChampionshipValidated'
            }
        ))
        assert len(c.events) == 2
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'ready'

        c.add_event(ChampionshipEvent.championship_started(championship_id))
        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'started'

        c.add_event(ChampionshipEvent.championship_finished(championship_id))
        assert len(c.events) == 4
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'finished'

    def test_workflow_invalid_championship(self):
        championship_id = uuid4()
        name = 'Roborumble'
        c = Championship(championship_id)
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        c.add_event(ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots))
        assert len(c.events) == 1
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'pending'

        c.add_event(ChampionshipEvent.decode(
                {
                    'id': str(uuid4()),
                    'championship_id': str(championship_id),
                    'created_at': datetime.utcnow().isoformat(),
                    'event': 'ChampionshipInvalidated'
                }
            ))
        assert len(c.events) == 2
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'invalid'

        c.add_event(ChampionshipEvent.championship_deleted(championship_id))
        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'deleted'

    def test_start(self):
        championship_id = uuid4()
        name = 'Roborumble'
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        event_list = [
            ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots),
            ChampionshipEvent.decode(
                {
                    'id': str(uuid4()),
                    'championship_id': str(championship_id),
                    'created_at': datetime.utcnow().isoformat(),
                    'event': 'ChampionshipValidated'
                }
            ),
        ]

        c = Championship(championship_id)
        for e in event_list:
            c.add_event(e)

        c.start()
        assert len(c.events) == 3
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'started'
        assert c.current_state.robots == robots

    def test_finish(self):
        championship_id = uuid4()
        name = 'Roborumble'
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        event_list = [
            ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots),
            ChampionshipEvent.decode(
                {
                    'id': str(uuid4()),
                    'championship_id': str(championship_id),
                    'created_at': datetime.utcnow().isoformat(),
                    'event': 'ChampionshipValidated'
                }
            ),
            ChampionshipEvent.championship_started(championship_id),
        ]

        c = Championship(championship_id)
        for e in event_list:
            c.add_event(e)

        c.finish()
        assert len(c.events) == 4
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'finished'
        assert c.current_state.robots == robots

    def test_delete(self):
        championship_id = uuid4()
        name = 'Roborumble'
        robots = [uuid4(), uuid4(), uuid4(), uuid4(), uuid4()]
        event_list = [
            ChampionshipEvent.championship_created(championship_id, 'Roborumble', robots),
            ChampionshipEvent.decode(
                {
                    'id': str(uuid4()),
                    'championship_id': str(championship_id),
                    'created_at': datetime.utcnow().isoformat(),
                    'event': 'ChampionshipValidated'
                }
            ),
            ChampionshipEvent.championship_started(championship_id),
        ]

        c = Championship(championship_id)
        for e in event_list:
            c.add_event(e)

        c.delete()
        assert len(c.events) == 4
        assert c.current_state.id == championship_id
        assert c.current_state.name == name
        assert c.current_state.status == 'deleted'
        assert c.current_state.robots == robots
