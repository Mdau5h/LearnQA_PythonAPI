import requests

url = 'https://playground.learnqa.ru/api/'

request_types = [
    'GET',
    'POST',
    'PUT',
    'DELETE'
]


def get_response(type, url, params=None, data=None):
    return requests.request(type, url + 'compare_query_type', params=params, data=data)


for type in request_types:
    for method in request_types:
        if type == 'GET':
            compare = get_response(type, url, params={'method': method})
        else:
            compare = get_response(type, url, data={'method': method})
        print(f'{type=}, {method=}')
        if method != type and 'success' in compare.text:
            print(f'Обнаружено расхождение: {type=}, {method=}')