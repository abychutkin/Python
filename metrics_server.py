# Программа представляющая собой сервер хранения различных метрик.
# Взаимодействие с клиетами прозводится с помощью простого текстового
# протокола.
# Сервер должен обрабатывать команды get и put.


import asyncio


class MetricsStorage:
    """
    Класс для хранения и выдачи метрик, может принимать или же возвращать
    метрики в ответ на команды от клиента.
    У каждой команды есть своя структура, при нарушении которой выдается
    сообщение об ошибке:
    error\nwrong command\n\n
    """
    def __init__(self):
        self.metrics = {}
        # Перечень обрабатываемых команд, на случай если добавятся еще команды
        self.commands = {'put': self.put, 'get': self.get}

    @staticmethod
    def combine_elements(key, iterable):
        """
        Метод принимает ключ и список кортежей, в результате объединяет ключ и
        элементы кортежа в строку
        """
        data = []
        for item in iterable:
            data.append('{} {}'.format(key, ' '.join(map(str, item))))
        return '\n'.join(data)

    def get(self, key):
        """
        Метод выполняет команду get.
        У данной команды следующая структура:
        get <key>\n
        В качестве ключа может быть указана *, в таком случае нужно вернуть
        все метрики.
        Ответ должен начинаться ok\n и завершаться \n\n.
        Если метрики на сервере нет, то нужно вернуть ok\n\n
        При нарушении протокола возвращается сообщение об ошибке
        """

        if key == '*':
            elements = (self.combine_elements(k, self.metrics[k])
                        for k in self.metrics)
            result = '\n'.join(elements)
        else:
            result = self.combine_elements(key, self.metrics.get(key, []))

        return 'ok{}\n\n'.format('\n' + result)

    def put(self, data):
        """
        Метод выполняет команду put
        У данной команды следующая структура:
        put <key> <value> <timestamp>\n
        Нужно также учитывать то, что у одного ключа метрики может быть
        несколько значений
        timestamp преобразуется в int
        value преобразовывается в float
        """
        # Проверяется структура команды put и разбивается на части, при
        # нарушении протокола возвращается сообщение об ошибке
        data = data.split(' ')
        if len(data) != 3:
            return 'error\nwrong command\n\n'

        try:
            key = data[0].strip()
            value = float(data[1])
            timestamp = int(data[2])
        except ValueError:
            return 'error\nwrong command\n\n'

        if key not in self.metrics:
            self.metrics[key] = [(value, timestamp)]
        else:
            if (value, timestamp) not in self.metrics[key]:
                self.metrics[key].append((value, timestamp))
                self.metrics[key].sort(key=lambda item: item[1])

        return 'ok\n\n'

    def process_data(self, data):
        """
        Метод выполняющий первоначальную обработку команды и вызов
        нужного метода
        """
        try:
            command, data = data.split(' ', maxsplit=1)
        except ValueError:
            return 'error\nwrong command\n\n'

        # Обработка неправильной команды для которой нет нужной функции
        function = self.commands.get(command)
        if not function:
            return 'error\nwrong command\n\n'

        result = function(data.strip())
        return result


class ClientServerProtocol(asyncio.Protocol):
    metrics = MetricsStorage()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = type(self).metrics.process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
