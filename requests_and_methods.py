import requests

url = 'https://playground.learnqa.ru/api/'

methods = {
    'compare': 'compare_query_type'
}

compare = requests.request("GET", url + methods['compare'])
print(compare.text)
