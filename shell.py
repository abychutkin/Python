import socket
import subprocess


def auth(client_socket):
    """Функция осуществляет авторизацию на шелл"""
    username = b'admin'
    passw = b'123'
    # Ввод неправильного логина или пароля допускается 3 раза, а затем
    # прием данных завершается
    for _ in range(3):
        client_socket.send(b'Login: ')
        login = client_socket.recv(BUFFSIZE)[:-1]
        client_socket.send(b'Password: ')
        password = client_socket.recv(BUFFSIZE)[:-1]
        if login == username and password == passw:
            return True
    return False


def client_work(client_socket):
    """Функция выполняет основную работу - принимает и выполняет команды"""
    while True:
        client_socket.send(b'cmd: ')
        command = client_socket.recv(BUFFSIZE)
        if not command or command[:-1] == b'exit':
            break
        # Благодаря модулю subprocess получаем вывод после выполнения
        # команды и он отправляется пользователю
        output = subprocess.getoutput(command).encode()
        client_socket.send(output + b'\n')
    client_socket.close()


HOST = ''
PORT = 4452
BUFFSIZE = 1024
ADDR = (HOST, PORT)

print('To finish program press CTRL + C')

# Используется диспетчер контекста, чтобы не пришлось самостоятельно
# закрывать сокет сервера
with socket.socket() as server:
    # Порт можно использовать после завершения скрипта
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Привязка сервера к адресу и его запуск
    server.bind(ADDR)
    server.listen(5)
    
    # Изначально клиентского сокета нет
    connection = None

    while True:
        # Завершение программы происходит при нажатии CTRL + C
        try:
            # Получение клиентского сокета
            connection = server.accept()[0]
            # Если авторизация не пройдена, то клиентский сокет закрывается
            if auth(connection):
                client_work(connection)
            else:
                connection.close()
        except KeyboardInterrupt:
            # Вывод пустой строки просто для красоты, чтобы переносить
            # приглашение для ввода в консоли после ^C
            print()
            # Используется особенность булевых выражений в Python, если
            # connection все еще None, то клиентского сокета нет и закрывать
            # его не нужно
            connection and connection.close()
            break
