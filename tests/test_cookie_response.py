import requests

class TestCookie():

    def setup(self):
        self.url = "https://playground.learnqa.ru/api/homework_cookie"

    def test_cookie(self):
        get_cookie = requests.get(self.url)
        assert get_cookie.status_code == 200, f"Error {get_cookie.status_code}. Response text is '{get_cookie.text}"
        cookie_dict = get_cookie.cookies.get_dict()
        if cookie_dict == {}:
            assert False, f"Cookie is empty. Response text is '{get_cookie.text}''"
        print(cookie_dict)
