import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):


    exclude_params = {
        'password': '123',
        'username': 'learnqa',
        'firstName': 'learnqa',
        'lastName': 'learnqa'
    }

    # Успешное создание пользователя
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test creates user successfully")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    # Создание пользователя с уже существующим емейлом
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test creates user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    # Создание пользователя с емейлом без символа @
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test creates user with email without '@' symbol")
    def test_create_user_with_incorrect_email(self):

        email = 'vinkotovexample.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == 'Invalid email format', f"Unexpected response content {response.content}"

    # Создание пользователя без одного необходимого поля

    @pytest.mark.parametrize('field_to_delete', exclude_params)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test creates user without required fields")
    def test_create_user_without_one_field(self, field_to_delete):

        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        data.pop(field_to_delete)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'The following required params are missed: {field_to_delete}', f"User created without required field: '{field_to_delete}'"

    # Создание пользователя с очень коротким именем
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test creates user with short name")
    def test_create_user_with_short_firstname(self):
        email = 'vinkotov@example.com'

        data = self.prepare_registration_data(email)
        data["firstName"] = 'a'
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'firstName' field is too short", f"User created with 'firstName' being too short"

    # Создание пользователя с очень длинным именем
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test creates user with very long name")
    def test_create_user_with_long_firstname(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        data["firstName"] = 'a'*251
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'firstName' field is too long", f"User created with 'firstName' being too long"
