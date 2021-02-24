from uuid import uuid4

from robot_service.infra.db import db, UUID
from robot_service.infra.upload import robot_files


class Robot(db.Model):
    __tablename__ = 'robot'

    id = db.Column(UUID, primary_key=True, default=uuid4)
    name = db.Column(db.VARCHAR(64), nullable=False)
    file_name = db.Column(db.VARCHAR(64), nullable=False)


class RobotDomain:
    _robot: Robot = None

    def __init__(self, robot: Robot = None, robot_id: UUID = None, name: str = None):
        if robot:
            self._robot = robot
        else:
            if robot_id and name:
                self._robot = Robot()
                self._robot.id = robot_id
                self._robot.name = name

    @property
    def robot(self):
        return self._robot

    def add_file(self, file):
        file_name = robot_files.save(file)
        self._robot.file_name = file_name

    def serialize(self):
        if not self._robot:
            return {}
        return {
            'id': self._robot.id,
            'name': self._robot.name,
            'file_name': self._robot.file_name,
            'url': robot_files.url(self._robot.file_name)
        }
