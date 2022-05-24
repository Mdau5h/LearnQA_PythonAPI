import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    # Попытка удалить пользователя по ID = 2
    @allure.description("This test tries to delete protected user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_protected_user(self):
        # login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")
        print(login_response.content)
        user_id = self.get_json_value(login_response, "user_id")

        # delete
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid},
                                            )
        Assertions.assert_code_status(delete_response, 400)
        assert delete_response.content.decode(
            'utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"It is possible to delete protected user. Response content: '{delete_response.content}'"

    # Позитивный тест: создать, залогиниться, удалить, проверить
    @allure.description("This test create test user then login and delete it")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_positive(self):
        # create
        test_data = self.prepare_registration_data()
        create_response = MyRequests.post("/user/", data=test_data)
        Assertions.assert_code_status(create_response, 200)
        Assertions.assert_json_has_key(create_response, 'id')

        # login
        login_response = MyRequests.post("/user/login", data=test_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")
        user_id = self.get_json_value(login_response, "user_id")
        # print(user_id)
        # print(login_response.content)

        # delete
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid},
                                            )

        # print(delete_response.content)
        Assertions.assert_code_status(delete_response, 200)
        assert delete_response.content.decode(
            'utf-8') == '', \
            f"Unexpected content. Response content: '{delete_response.content}'"


        # get
        check_response = MyRequests.get(f"/user/{user_id}",
                                        headers={'x-csrf-token': token},
                                        cookies={'auth_sid': auth_sid}
                                        )
        # print(check_response.content)
        Assertions.assert_code_status(check_response, 404)
        assert check_response.content.decode(
            'utf-8') == 'User not found', f"Unexpected content. Response content: '{delete_response.content}'"

    # Попытка удалить пользователя из-под другого пользователя
    @allure.description("This test tries to delete user with being authorised by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_wrong_auth(self):
        # create
        test_data = self.prepare_registration_data()
        create_response = MyRequests.post("/user/", data=test_data)
        Assertions.assert_code_status(create_response, 200)
        Assertions.assert_json_has_key(create_response, 'id')

        # login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")

        # delete
        user_id = self.get_json_value(create_response, "id")
        # print(login_response.content)

        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid},
                                            )
        # print(delete_response.url)
        # print(delete_response.content)
        Assertions.assert_code_status(delete_response, 400)
        assert delete_response.content.decode(
            'utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected content. Response content: '{delete_response.content}'"
