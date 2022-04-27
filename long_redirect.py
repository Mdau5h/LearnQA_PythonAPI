import requests

url = 'https://playground.learnqa.ru/api/'

method = 'long_redirect'
response = requests.post(url + method)
print(f"Количество редиректов: {len(response.history) - 1}\nИтоговый URL: {response.history[-1].headers['location']}")