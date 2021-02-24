from robot_service.data.events import RobotEvent
from robot_service.domain.robot import Robot, RobotDomain
from robot_service.infra.db import db
from robot_service.infra.kafka import robot_message_sender


class Repository:

    @classmethod
    def get(cls, robot_id=None):
        query = Robot.query
        if robot_id:
            if not isinstance(robot_id, list):
                return RobotDomain(query.get(robot_id))
            else:
                query = query.filter(Robot.id.in_(robot_id))

        return [RobotDomain(r) for r in query.all()]

    @classmethod
    def save(cls, domain: RobotDomain):
        if domain.robot:
            try:
                db.session.add(domain.robot)
                db.session.commit()
                robot_message_sender.send(
                    RobotEvent.robot_created(domain)
                )
            except Exception as err:
                db.session.rollback()
                raise err

    @classmethod
    def delete(cls, robot_id):
        robot = Robot.query.get(robot_id)
        if robot:
            try:
                db.session.delete(robot)
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                raise err
