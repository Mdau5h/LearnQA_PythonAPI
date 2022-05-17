from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        responce = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(responce, "username")
        Assertions.assert_json_has_no_key(responce, "email")
        Assertions.assert_json_has_no_key(responce, "firstName")
        Assertions.assert_json_has_no_key(responce, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        auth_response = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(auth_response, 'auth_sid')
        token = self.get_header(auth_response, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(auth_response, "user_id")

        check_response = MyRequests.get(f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_fields = [
            'username',
            'email',
            'firstName',
            'lastName'
        ]

        Assertions.assert_json_has_keys(check_response, expected_fields)

