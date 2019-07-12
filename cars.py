# Программа для демонстрации использования наследования и
# классовых методов.
# Программа должна из csv файла считывать информацию
# о машинах и создавать объекты нужного класса.
# Строки в файле могут быть некорректны и в таком
# случае они игнорируются

import abc
import csv
import os


class BaseCar(abc.ABC):
    """
    Базовый класс для всех машин
    """

    @abc.abstractmethod
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        """
        Метод возвращает расширение фото машины
        """
        return os.path.splitext(self.photo_file_name)[-1]

    @classmethod
    def get_unique_att(cls):
        """
        Метод возвращающий название уникальногой аттрибута класса
        """
        return cls.unique_att


class Car(BaseCar):
    """
    Класс легкового автомобиля
    """
    unique_att = 'passenger_seats_count'
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(BaseCar):
    """
    Класс грузового автомобиля
    """
    unique_att = 'body_whl'
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        # Извлечение длины, ширины и высоты кузова
        data = body_whl.split('x')
        # Если размеры кузова не указаны, то они устанавливаются в значение 0
        if len(data) == 1 and not data[0]:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        elif len(data) == 3:
            self.body_length = float(data[0])
            self.body_width = float(data[1])
            self.body_height = float(data[2])
        else:
            raise ValueError

    def get_body_volume(self):
        """
        Метод возвращает объем кузова
        """
        return self.body_length * self.body_width * self.body_height


class SpecMachine(BaseCar):
    """
    Класс спецмашины
    """
    unique_att = 'extra'
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def row_to_dict(row):
    """
    Функция для преобразования строки из файла в словарь,
    в ней также учитывается то, что порядок столбцов в файле может
    меняться
    """
    result = {}
    for index, key in enumerate(row_to_dict.header):
        result[key] = row[index]
    result['carrying'] = float(result['carrying'])
    return result


def get_car_list(csv_filename):
    """
    Функция для обработки csv файла и преобразования его
    строк в объекты соответствующего класса
    """
    car_classes = {'car': Car, 'truck': Truck,
                   'spec_machine': SpecMachine}
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        # Аттрибут функции, который выступает в качестве
        # статической переменной, чтобы не использовать
        # глобальную переменную
        row_to_dict.header = next(reader)

        for row in reader:
            # В обработке исключения учитывается то, что поле carrying должно
            # преобразовываться в float и у объема кузова грузового автомобиля
            # должна быть правильная структура - пустая строка или 3 измерения
            try:
                # Проверяется наличие всех столбцов в строке
                if len(row_to_dict.header) == len(row):
                    data = row_to_dict(row)
                else:
                    continue
                # Значения обязательных полей
                required = [data['brand'], data['photo_file_name'],
                            data['carrying']]
                car_class = car_classes[data['car_type']]
                unique = data[car_class.get_unique_att()]
                car_list.append(car_class(*required, unique))
            except ValueError:
                pass
    return car_list
