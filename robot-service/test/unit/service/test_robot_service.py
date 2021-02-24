from unittest.mock import patch
from uuid import uuid4


from robot_service.domain.robot import Robot
from robot_service.domain.repository import Repository
from robot_service.service.robot import check_robots_existence


class TestRobotService:

    @patch('robot_service.service.robot.Repository', autospec=Repository)
    def test_check_robots(self, mocked_repo):
        mocked_repo.get.return_value = []
        ans = check_robots_existence([uuid4()])
        assert not ans

    @patch('robot_service.service.robot.Repository', autospec=Repository)
    def test_check_robots_true(self, mocked_repo):
        ids = [uuid4(), uuid4(), uuid4()]
        mocked_repo.get.return_value = [Robot(), Robot(), Robot()]
        ans = check_robots_existence(ids)
        assert ans
