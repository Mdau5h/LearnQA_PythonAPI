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
]

for type in request_types:
    if type == 'GET':
        compare = requests.request(type, url + methods['compare'], params={'method': type})
    else:
        compare = requests.request(type, url + methods['compare'], data={'method': type})
    print(type)
    print(compare)