# Скрипт предназначен для обнаружения открытых портов и получения баннеров
# сервисов, работающих на обнаруженных портах.
# Если сервис не возвращает баннер, то делается предположение о запущенном
# сервисе исходя из номера порта.


import argparse
import os
import socket


def check_port_is_open(host, port):
    """Функция проверяет открыт ли порт на заданном хосте"""
    with socket.socket() as sock:
        return sock.connect_ex((host, port))


def get_banner(host, port):
    """Функция пробует получить баннер от сервиса, если сервис не выдает
    баннер, то возвращается пустая строка"""
    try:
        with socket.create_connection((host, port), 1) as sock:
            banner = sock.recv(1000)
            return banner.decode(errors='replace').strip()
    except socket.timeout:
        return ''


def scanner(host, port):
    """Функция проверяющая порт на заданном хосте"""
    state = check_port_is_open(host, port) == 0
    print(port, end='\t')
    if state:
        print('open', end='\t')
        banner = get_banner(host, port)
        if not banner:
            for key in PORTS_AND_SERVICES:
                if port in key:
                    banner = PORTS_AND_SERVICES[key]
        print(banner)
    else:
        print('closed')


parser = argparse.ArgumentParser(description='Simple Banner Grabbing Script',
                                 usage='You should specify host and port/'
                                 'ports to scan')

parser.add_argument('-H', dest='target_host', action='store',
                    help='Remote host')

# Опции -p и -P являются взаимоисключающимися
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', dest='target_port', action='store', type=int,
                   help='Port to scan')
group.add_argument('-P', dest='target_ports', action='store',
                   help='Ports to scan')

args = parser.parse_args()
target_host = args.target_host

if target_host is None or (args.target_port is None and
                           args.target_ports is None):
    print(parser.usage)
    exit(0)

if args.target_port:
    target_ports = [args.target_port]

else:
    target_ports = []
    for ports in args.target_ports.split(','):
        # Если значением опции -P является минус, то проверяются все порты
        if ports == '-':
            target_ports = list(range(65536))
            break
        # Проверка диапазона портов
        elif '-' in ports:
            borders = [int(border) for border in ports.split('-')]
            for port in range(borders[0], borders[1]+1):
                target_ports.append(port)
        else:
            target_ports.append(int(ports))

try:
    # У этой строки два назначения: преобразование имени хоста в ip адрес и
    # фильтрация специальных символов для избежания инъекции в команду
    target_ip = socket.gethostbyname(target_host)
except socket.gaierror:
    print("[-] Cannot resolve '{0}': Unknown host".format(target_host))
    exit()

# Проверка работоспособности хоста с помощью команды ping, вывод от данной
# команды направляется в /dev/null
COMMAND_OUTPUT = '/dev/null'
host_state = os.system('ping -c 1 -w 1 {} > {}'.format(target_ip,
                       COMMAND_OUTPUT))

# Перечень сервисов и соответствующих им портов
PORTS_AND_SERVICES = {(20, 21): 'FTP', (22,): 'SSH', (23,): 'Telnet',
                      (25,): 'SMTP', (53,): 'DNS', (67, 68): 'DHCP',
                      (69,): 'TFTP', (80,): 'HTTP', (110,): 'POP3',
                      (119,): 'NNTP', (123,): 'NTP', (143,): 'IMAP4',
                      (389,): 'LDAP', (443,): 'HTTPS', (993,): 'IMAPS',
                      (1812,): 'RADIUS', (5190,): 'AIM'}

if host_state == 0:
    print('PORT\tSTATE\tSERVICE')
else:
    print("Host: '{}' is unreachable".format(host))
for port in target_ports:
    scanner(target_ip, port)
