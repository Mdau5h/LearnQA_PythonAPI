from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdut(BaseCase):
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
