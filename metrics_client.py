# Данная программа является клиентом, взаимодействующим с сервером, хранящим
# различные метрики. Клиент и сервер взаимодействуют с помощью простого
# текстового протокола


import socket
import time


class ClientError(Exception):
    """
    Исключение возникающее у клиента, при нарушении протокола
    """
    pass


class ServerError(Exception):
    """
    Исключение возникающее, если данные на сервере сохранены в
    неправильном формате
    """
    pass


class Client:
    """
    Класс клиента для работы с сервером, обрабатывающий метрики,
    которыми могут быть различные аналитические данные, например,
    размер используемой памяти, количество пользователей и т.д.
    host - ip адрес сервера
    port - порт для подключения
    timeout - необязательный параметр, таймаут соединения,
    по-умолчанию его значение None
    """
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.__connection = socket.create_connection((host, port),
                                                         timeout)
        except socket.error as error:
            raise ClientError("Can't establish connection to server.")
        except socket.timeout:
            raise ServerError("Connection timeout exceeded.")

    def __send_data(self, data):
        """
        Метод для отправки данных на сервер, используется для работы методов
        put и get
        data - сообщение, которое нужно отправить на сервер
        """
        try:
            self.__connection.send(data.encode('utf8'))
            resp = self.__connection.recv(1024)
        except socket.error as err:
            print('Произошла сетевая ошибка:', err)

        resp = resp.decode('utf8')

        # Сервер сообщил о нарушении протокола
        if resp == 'error\nwrong command\n\n':
            raise ClientError

        return resp

    def stop(self):
        """
        Метод для завершения работы клиента, закрывающий клиентский сокет
        """
        self.__connection.close()

    def put(self, metric_name, metric_value, timestamp=time.time()):
        """
        Метод отправки метрики
        metric_name - название метрики
        metric_value - значение метрики
        timestamp - необязательный параметр, содержищий временную метку
        """
        data = 'put {} {} {}\n'.format(metric_name, metric_value, timestamp)
        self.__send_data(data)

    def get(self, metric_name):
        """
        Метод для получения метрик с сервера, которые представлены в виде
        словаря, если метрики на сервере нет, то метод вернет пустой словарь.
        При нарушении протокола будет вызвано исключение ClientError.
        metric_name - имя метрики
        """
        data = 'get {}\n'.format(metric_name)
        resp = self.__send_data(data)

        # Метрики на сервере нет
        if resp == 'ok\n\n':
            return {}

        # Уборка лишнего из ответа, ответ начинается с 'ok\n' и
        # заканчивается переносом строки и ответ разделяется по символу
        # переноса строки
        resp = resp[3:-2].split('\n')
        result = {}

        for item in resp:
            # Ответ состоит из названия метрики, ее значения и
            # метки времени, также добавлена проверка формата ответа сервера,
            # если метрика составлена неправильно то вызывается исключение
            # ServerError
            try:
                key, value, timestamp = item.split(' ')
                value = float(value)
                timestamp = int(timestamp)
            except ValueError:
                raise ServerError

            # У одной метрики может быть несколько значений
            result.setdefault(key, []).append((timestamp, value))
        return result
