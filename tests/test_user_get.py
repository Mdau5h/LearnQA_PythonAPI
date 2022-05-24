import allure


from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Get user tests")
class TestUserGet(BaseCase):

    @allure.description("This test gets user detail with no authorisation")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_user_details_not_auth(self):
        fields_response_should_not_have = [
            "email",
            "firstName",
            "lastName"
        ]

        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_keys(response, fields_response_should_not_have)

    @allure.description("This test gets user detail with being authorised as this user")
    @allure.severity(allure.severity_level.BLOCKER)
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

    @allure.description("This test gets user detail with being authorised as another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_another_user(self):
        # auth
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        fields_response_should_not_have = [
            "email",
            "firstName",
            "lastName"
        ]
        user_id_to_check = 1
        auth_response = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(auth_response, 'auth_sid')
        token = self.get_header(auth_response, "x-csrf-token")
        assert user_id_to_check != self.get_json_value(auth_response, "user_id"), "You authorised as the same user you trying to check"
        # get user
        check_response = MyRequests.get(f"/user/{user_id_to_check}",
                                        headers={'x-csrf-token': token},
                                        cookies={'auth_sid': auth_sid}
                                        )
        Assertions.assert_json_has_key(check_response, "username")
        Assertions.assert_json_has_no_keys(check_response, fields_response_should_not_have)


