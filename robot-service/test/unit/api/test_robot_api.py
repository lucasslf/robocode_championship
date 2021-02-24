from unittest.mock import patch
from uuid import uuid4

from pytest import fail

from robot_service.api.robot import _validate_new_robot_data


class TestRobotService:

    def test_validate_robot_data_name_is_required(self):
        data = {'test': 'test'}
        files = {'file': 'adsdsd'}
        try:
            _validate_new_robot_data(data, files)
        except Exception as e:
            assert str(e) == 'Robot name is required'
        else:
            fail('Did not raise Exception')

    def test_validate_robot_data_file_is_required(self):
        data = {'name': 'test'}
        files = {'photo': 'adsdsd'}
        try:
            _validate_new_robot_data(data, files)
        except Exception as e:
            assert str(e) == 'Robot jar file is required'
        else:
            fail('Did not raise Exception')
