import socket
from threading import Thread
from logic import game
from players import Player


def process_connection(client_conn):
    with client_conn:
        player = Player(client_conn)
        try:
            game(player)
        except OSError:
            pass


with socket.socket() as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 5002))
    sock.listen(5)
    while True:
        client_conn = sock.accept()[0]
        th = Thread(target=process_connection, args=(client_conn,))
        th.start()
