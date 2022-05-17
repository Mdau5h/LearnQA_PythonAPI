import requests

class TestCookie():

    def setup(self):
        self.url = "https://playground.learnqa.ru/api/homework_cookie"

    def test_cookie(self):
        cookie_responce = requests.get(self.url)
        assert cookie_responce.status_code == 200, f"Error {cookie_responce.status_code}. Response text is '{cookie_responce.text}"
        cookie_dict = cookie_responce.cookies
        if cookie_dict == {}:
            assert False, f"Cookie is empty. Response text is '{cookie_responce.text}''"
        print(cookie_dict)
