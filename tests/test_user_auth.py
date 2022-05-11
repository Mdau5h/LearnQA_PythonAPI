import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        self.url = "https://playground.learnqa.ru/api/user/"
        self.methods = {
            'login': "login",
            'check_id': "auth"
        }

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        login = requests.post(self.url + self.methods['login'], data=data)

        self.auth_sid = self.get_cookie(login, "auth_sid")
        self.token = self.get_header(login, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(login, "user_id")

    def test_auth_user(self):
        check_id = requests.get(
            self.url + self.methods['check_id'],
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            check_id,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            check_id = requests.get(
                self.url + self.methods['check_id'],
                headers={"x-csrf-token": self.token}
            )
        elif condition == "no_token":
            check_id = requests.get(
                self.url + self.methods['check_id'],
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            check_id,
            "user_id",
            0,
            f"User authorised with condition {condition}"
        )
