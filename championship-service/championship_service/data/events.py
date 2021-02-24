from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class BattleEvent:
    id: UUID
    battle_id: UUID
    championship_id: UUID
    robot_1: UUID
    robot_2: UUID
    created_at: datetime
    event: str

    @classmethod
    def battle_created(cls, championship_id: UUID, robot_1: UUID, robot_2: UUID):

        return cls(
            id=uuid4(),
            battle_id=uuid4(),
            championship_id=championship_id,
            robot_1=robot_1,
            robot_2=robot_2,
            created_at=datetime.utcnow(),
            event='BattleCreated',
        )

    @classmethod
    def decode(cls, message):
        return cls(
            id=UUID(message['id']),
            battle_id=UUID(message['battle_id']),
            championship_id=UUID(message['championship_id']),
            robot_1=UUID(message['robot_1']),
            robot_2=UUID(message['robot_2']),
            created_at=datetime.fromisoformat(message['created_at']),
            event=message['event'],
        )


@dataclass
class ChampionshipEvent:
    id: UUID
    championship_id: UUID
    championship_name: Optional[str]
    robots: Optional[list]
    created_at: datetime
    event: str

    @classmethod
    def championship_created(cls, championship_id: UUID, championship_name: str, robots: list):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            championship_name=championship_name,
            robots=robots,
            created_at=datetime.utcnow(),
            event='ChampionshipCreated',
        )

    @classmethod
    def championship_started(cls, championship_id: UUID, robots: list):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            championship_name=None,
            robots=robots,
            created_at=datetime.utcnow(),
            event='ChampionshipStarted',
        )

    @classmethod
    def championship_finished(cls, championship_id: UUID):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            championship_name=None,
            robots=None,
            created_at=datetime.utcnow(),
            event='ChampionshipFinished',
        )

    @classmethod
    def championship_deleted(cls, championship_id: UUID):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            championship_name=None,
            robots=None,
            created_at=datetime.utcnow(),
            event='ChampionshipDeleted',
        )

    @classmethod
    def decode(cls, message):
        return cls(
            id=UUID(message['id']),
            championship_id=UUID(message['championship_id']),
            championship_name=(
                message['championship_name'] if 'championship_name' in message else None
            ),
            robots=(
                [UUID(robot_id) for robot_id in message['robots']]
                if message.get('robots') else None
            ),
            created_at=datetime.fromisoformat(message['created_at']),
            event=message['event'],
        )
