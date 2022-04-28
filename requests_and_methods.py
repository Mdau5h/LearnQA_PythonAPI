import requests

url = 'https://playground.learnqa.ru/api/'

methods = {
    'compare': 'compare_query_type'
}

compare = requests.request("HEAD", url + methods['compare'])
print(compare.text)
print(compare.status_code)

