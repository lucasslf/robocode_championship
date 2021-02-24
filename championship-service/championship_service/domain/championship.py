import abc
from abc import abstractmethod
from dataclasses import dataclass
from logging import getLogger
from typing import Optional
from uuid import UUID

from championship_service.data.events import ChampionshipEvent
from championship_service.infra.kafka import ChampionshipKafkaProducer, ChampionshipKafkaConsumer


@dataclass
class CurrentState:
    id: Optional[UUID]
    name: Optional[str]
    status: Optional[str]
    robots: Optional[list]


class Championship:

    events: list

    current_state: CurrentState

    _unflushed_index = 0

    def __init__(self, championship_id):
        self.id = championship_id
        self.events = []
        self.current_state = CurrentState(championship_id, None, 'transient', [])

    @classmethod
    def create(cls, championship_id, championship_name, robots):
        championship = cls(championship_id)
        championship.add_event(
            ChampionshipEvent.championship_created(championship_id, championship_name, robots)
        )
        return championship

    def start(self):
        if self.current_state.status != 'ready':
            raise Exception('Invalid action')
        self.add_event(
            ChampionshipEvent.championship_started(
                self.current_state.id,
                self.current_state.robots
            )
        )

    def finish(self):
        if self.current_state.status != 'started':
            raise Exception('Invalid action')
        self.add_event(
            ChampionshipEvent.championship_finished(self.current_state.id)
        )

    def delete(self):
        self.add_event(
            ChampionshipEvent.championship_deleted(self.current_state.id)
        )

    def add_event(self, championship_event: ChampionshipEvent, loading=False):
        if championship_event.event == 'ChampionshipCreated':
            self.current_state.name = championship_event.championship_name
            self.current_state.robots = championship_event.robots
            self.current_state.status = 'pending'
        elif championship_event.event == 'ChampionshipStarted':
            self.current_state.status = 'started'
        elif championship_event.event == 'ChampionshipFinished':
            self.current_state.status = 'finished'
        elif championship_event.event == 'ChampionshipInvalidated':
            self.current_state.status = 'invalid'
        elif championship_event.event == 'ChampionshipValidated':
            self.current_state.status = 'ready'
        elif championship_event.event == 'ChampionshipDeleted':
            self.current_state.status = 'deleted'

        self.events.append(championship_event)
        if loading:
            self._unflushed_index = len(self.events)

    def get_events_to_flush(self):
        return [self.events[i] for i in range(self._unflushed_index, len(self.events))]


class ChampionshipRepository(abc.ABC):
    
    @abstractmethod
    def get(self, championship_id: UUID):
        pass

    @abstractmethod
    def save(self, championship: Championship):
        pass
    
    
class ChampionshipEventRepository(ChampionshipRepository):

    def __init__(self, event_store: ChampionshipKafkaConsumer, publisher: ChampionshipKafkaProducer):
        self._event_store = event_store

        self._publisher = publisher

    def get(self, championship_id: UUID):
        
        all_events = self._event_store.get_all_events()
        events = [
            e for e in all_events
            if 'championship_id' in e and e['championship_id'].lower() == str(championship_id)
        ]
        championship = Championship(championship_id)
        for e in events:
            championship.add_event(ChampionshipEvent.decode(e), loading=True)

        return championship
    
    def save(self, championship: Championship):
        for e in championship.get_events_to_flush():
            self._publisher.send(e)
