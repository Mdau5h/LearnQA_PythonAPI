import requests

class TestCookie():

    def setup(self):
        self.url = "https://playground.learnqa.ru/api/homework_header"

    def test_cookie(self):
        header_responce = requests.get(self.url)
        assert header_responce.status_code == 200, f"Error {header_responce.status_code}. Response text is '{header_responce.text}"
        headers_dict = header_responce.headers
        if headers_dict == {}:
            assert False, f"Headers are empty. Response text is '{header_responce.text}''"
        print(headers_dict)
