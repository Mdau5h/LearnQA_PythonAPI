import pytest
import requests
import test_old.data_to_test as d
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAgent(BaseCase):

    def setup(self):
        self.url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        self.fields_to_check = [
            'platform',
            'browser',
            'device'
        ]

    @pytest.mark.parametrize('user_agent, expected_result', list(map(tuple, d.user_agent_values.items())))
    def test_use_agent(self, user_agent, expected_result):
        user_agent_responce = requests.get(self.url, headers={"User-Agent": user_agent})
        assert user_agent_responce.status_code == 200, f"Error {user_agent_responce.status_code}. Response text is '{user_agent_responce.text}"
        # print(user_agent_responce.text)
        for field in self.fields_to_check:
            Assertions.assert_json_value_by_name(user_agent_responce, field, expected_result[field], f"Response field '{field}' is wrong. Expected '{expected_result[field]}', got '{user_agent_responce.json()[field]}' instead.")
