from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4, UUID

from robot_service.domain.robot import RobotDomain
from robot_service.infra.db import UUID


@dataclass
class RobotEvent:
    id: UUID
    robot_id: UUID
    robot_name: str
    robot_url: str
    created_at: datetime
    event: str

    @classmethod
    def robot_created(cls, robot: RobotDomain):
        robot_data = robot.serialize()
        return cls(
            id=uuid4(),
            robot_id=robot_data['id'],
            robot_name=robot_data['name'],
            robot_url=robot_data['url'],
            created_at=datetime.utcnow(),
            event='RobotCreated',
        )


@dataclass
class ChampionshipEvent:
    id: UUID
    championship_id: UUID
    created_at: datetime
    event: str

    @classmethod
    def championship_invalidated(cls, championship_id):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            created_at=datetime.utcnow(),
            event='ChampionshipInvalidated',
        )

    @classmethod
    def championship_validated(cls, championship_id):

        return cls(
            id=uuid4(),
            championship_id=championship_id,
            created_at=datetime.utcnow(),
            event='ChampionshipValidated',
        )