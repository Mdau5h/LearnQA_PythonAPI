import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/'

methods = {
    'job_method': 'longtime_job',
}

# Получаем токен и время создания задачи
get_token = requests.get(url + methods['job_method'])
print(get_token.text)
token = get_token.json()['token']
time_offset = get_token.json()['seconds']

# Получаем статус задачи, когда она не готова
get_status = requests.get(url + methods['job_method'], params={'token': token})
print(get_status.text)
if get_status.json()['status'] == 'Job is NOT ready':
    print(f"Задача не готова, ожидайте {time_offset} секунд")

# Ждем указанное время и получаем статус еще раз
time.sleep(time_offset + 1)
get_status = requests.get(url + methods['job_method'], params={'token': token})
print(get_status.text)

# Проверка наличия полей
try:
    result = get_status.json()['result']
    if get_status.json()['status'] == 'Job is ready':
        print('Задача создана успешно')
    else:
        print('Задача не готова')
except:
    print('Нет поля "result"')


