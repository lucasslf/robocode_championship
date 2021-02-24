import uuid


from robot_service.domain.robot import RobotDomain
from robot_service.domain.repository import Repository


def add_robot(data, file):

    robot = RobotDomain(
        robot_id=uuid.uuid4(),
        name=data['name'],
    )
    robot.add_file(file)
    Repository.save(robot)
    return robot


def get_robots():
    robots = Repository.get()
    return robots


def get_robots_by_id(robot_id):
    robots = Repository.get(robot_id)
    return robots


def delete_robot(robot_id):
    Repository.delete(robot_id)


def check_robots_existence(robot_ids):
    robots = Repository.get(robot_ids)
    return len(robots) == len(robot_ids)
