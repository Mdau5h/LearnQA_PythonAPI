from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def setup(self):
        # Создаем тестового пользователя
        self.test_data = self.prepare_registration_data()
        print(self.test_data)
        self.create_response = MyRequests.post("/user/", data=self.test_data)
        Assertions.assert_code_status(self.create_response, 200)
        Assertions.assert_json_has_key(self.create_response, 'id')

    # Изменение данных только что созданного пользователя
    def test_edit_just_created_user(self):

        # Register
        register_data = self.prepare_registration_data()
        register_response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(register_response, 200)
        Assertions.assert_json_has_key(register_response, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(register_response, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        login_response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        edit_response = MyRequests.put(f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(edit_response, 200)

        # Get
        get_user_data_response = MyRequests.get(f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
        )

        Assertions.assert_json_value_by_name(
            get_user_data_response,
            'firstName',
            new_name,
            "Wrong name of the user after edit"
        )

    # Изменение данных пользователя, будучи неавторизованным
    def test_edit_user_not_auth(self):
        # edit
        user_id = self.get_json_value(self.create_response, "id")
        new_name = "Changed Name"
        edit_response = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(edit_response, 400)
        print(edit_response.content)
        assert edit_response.content.decode(
            'utf-8') == f"Auth token not supplied", f"User edited without authorisation. Response content: '{edit_response.content}'"

    # Изменение данных пользователя, будучи авторизованным другим пользователем
    def test_edit_user_auth_by_wrong_user(self):
        # login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_response = MyRequests.post("/user/login", data=login_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")

        # edit
        user_id = self.get_json_value(self.create_response, "id")
        print(user_id)
        new_name = "Changed Name"

        edit_response = MyRequests.put(f"/user/{user_id}",
                                       data={"firstName": new_name},
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       )
        Assertions.assert_code_status(edit_response, 400)
        assert edit_response.content.decode(
            'utf-8') == 'Please, do not edit test users with ID 1, 2, 3, 4 or 5.',\
            f"User edited with wrong token. Response content: '{edit_response.content}'"

    # Изменение email пользователя, будучи авторизованным тем же пользователем, на новый email без символа @
    def test_edit_user_incorrect_email(self):
        # login
        login_response = MyRequests.post("/user/login", data=self.test_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")

        # edit
        user_id = self.get_json_value(self.create_response, "id")
        print(user_id)
        new_email = 'vinkotovexample.com'

        edit_response = MyRequests.put(f"/user/{user_id}",
                                       data={"email": new_email},
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       )
        Assertions.assert_code_status(edit_response, 400)
        # print(edit_response.content)
        assert edit_response.content.decode(
            'utf-8') == 'Invalid email format', \
            f"User edited with incorrect email. Response content: '{edit_response.content}'"

    # Изменение firstName пользователя, будучи авторизованным тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_short_firstname(self):
        # login
        login_response = MyRequests.post("/user/login", data=self.test_data)
        token = self.get_header(login_response, 'x-csrf-token')
        auth_sid = self.get_cookie(login_response, "auth_sid")

        # edit
        user_id = self.get_json_value(self.create_response, "id")
        print(user_id)
        new_name = 'a'

        edit_response = MyRequests.put(f"/user/{user_id}",
                                       data={"firstName": new_name},
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       )
        Assertions.assert_code_status(edit_response, 400)
        # print(edit_response.content)
        assert edit_response.content.decode(
            'utf-8') == '{"error":"Too short value for field firstName"}', \
            f"User edited with short first name. Response content: '{edit_response.content}'"