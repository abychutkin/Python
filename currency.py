# Программа для пересчета курса валют с использованием web API и
# BeautifulSoup

from bs4 import BeautifulSoup
from decimal import Decimal


def get_course_in_rubles(page, valute):
    if valute == 'RUR':
        return Decimal(1)
    valute_data = page.find('CharCode', text=valute)
    nominal = int(valute_data.find_next_sibling('Nominal').text)
    value = valute_data.find_next_sibling('Value').text.replace(',', '.')
    value = Decimal(value)
    return value / nominal


def convert(amount, cur_from, cur_to, date, requests):
    bank_api = 'http://www.cbr.ru/scripts/XML_daily.asp'
    # Использовать переданный requests, так как сеть на проверяющем сервере
    # недоступна
    response = requests.get(bank_api, params={'date_req': date})
    page = BeautifulSoup(response.content, 'xml')
    amount *= get_course_in_rubles(page, cur_from)
    result = amount / get_course_in_rubles(page, cur_to)
    return result.quantize(Decimal('1.0000'))
