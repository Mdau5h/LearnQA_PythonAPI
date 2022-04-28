import requests

url = 'https://playground.learnqa.ru/api/'

methods = {
    'compare': 'compare_query_type'
}

request_types = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'HEAD'
]

compare = requests.request("GET", url + methods['compare'])
print(compare.text)



