# Данная программа представляет собой key-value storage. В зависимости от
# опций записывает значения в хранилище, либо читает из него. В данном случае
# хранилищем является файл. Одному ключу может соответствовать несколько
# значений.


import argparse
import os
import tempfile
import json


def get_data(path: str) -> None:
    """
    Функция извлекает данные из хранилища.
    Хранилище представляет собой файл, в котором хранится словарь,
    преобразованный в json.
    """
    # Обрабатываются случаи когда файл не существует или файл
    # существует, но он пустой
    try:
        with open(path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data


def read(data: dict, key: str) -> None:
    """
    Функция выводит значение или значения ключа,
    если ключ не существует - выводится None.
    data - словарь
    key - ключ
    """
    value = data.get(key, ['None'])
    print(', '.join(value))


def write(path: str, data: dict, key: str, value: str) -> None:
    """
    Функция записывает полученые значения в хранилище.
    data - словарь, который будет закодирован и записан в файл
    модулем json
    key - ключ, у которого может быть несколько значений
    value - значение которое будет добавлено в список существующего ключа,
    либо будет единственным элементом новосозданного списка
    """
    data.setdefault(key, []).append(value)
    with open(path, 'w') as f:
        json.dump(data, f)


parser = argparse.ArgumentParser()
parser.add_argument('--key', help='Specifies key for storing and retriving \
information from storage.')
parser.add_argument('--value', help='Specifies value for storing information,\
should be used together with --key option.')
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

data = get_data(storage_path)

if args.key:
    if args.value:
        write(storage_path, data, args.key, args.value)
    else:
        read(data, args.key)
else:
    parser.print_help()
