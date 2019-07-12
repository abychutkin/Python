"""
Программа для работы с API Вконтакте, суть которой заключается в подсчете
распределения возрастов друзей для указанного пользователя. Стоит отметить
то, что используется токен доступа, предоставленный преподавателями курса,
поэтому он жестко прописан в коде, но при необходимости можно переписать
принятие токена в функции в качестве аргумента или же получение из командной
строки.
"""

from collections import Counter
from datetime import date
from datetime import datetime
import requests


def get_user_id(TOKEN, uid):
    """
    Функция для получания id пользователя
    token - токен доступа
    uid - имя пользователя или его id
    """
    url = ('https://api.vk.com/method/users.get?v=5.71&'
           'access_token={}&user_ids={}'.format(TOKEN, uid))
    response = requests.get(url)
    data = response.json()
    return data['response'][0]['id']


def get_friends(TOKEN, uid):
    """
    Данная функция обрабатывает список друзей, результатом ее работы будет
    список из кортежей, каждый кортеж - это возраст и количество друзей с
    таким возрастом.
    Нужно отметить то, что по заданию возраст считается только учитывая год,
    не беря в расчет дни и месяцы.
    Результат сортируется по количеству друзей по убыванию и по возрастанию,
    исользуя возраст.
    """
    current_year = date.today().year
    url = ('https://api.vk.com/method/friends.get?v=5.71&'
           'access_token={}&user_id={}&fields=bdate'.format(TOKEN, uid))
    response = requests.get(url)
    data = response.json()
    ages = []
    for item in data['response']['items']:
        if 'bdate' in item:
            # У друзей может быть не указан год рождения
            try:
                bdate = datetime.strptime(item['bdate'], '%d.%m.%Y')
                ages.append(current_year - bdate.year)
            except ValueError:
                pass
    data = Counter(ages)
    result = [(age, quantity) for age, quantity in sorted(data.items(),
              key=lambda item: (item[1], -item[0]), reverse=True)]
    return result


def calc_age(uid):
    """
    Данная функция осуществляет общее управление и нужна по условию задания
    """
    # токен никогда не меняется и потому представлен константой
    TOKEN = ('17da724517da724517da72458517b8abce117'
             'da17da72454d235c274f1a2be5f45ee711')
    user_id = get_user_id(TOKEN, uid)
    return get_friends(TOKEN, user_id)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
