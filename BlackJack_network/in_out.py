# Модуль для вывода информации для игрока и получение от него каких-то данных.
# Можно было просто использовать print и обойтись без данного модуля, но он
# задумывался для того, чтобы в дальнейшем игра стала сетевой.
# Каждая функция принимает player, так как в дальнейшем в нем планируется
# хранить клиентский сокет.


def rules(player):
    """
    Функция для вывода правил игры
    """
    with open('rules.txt') as f:
        for line in f:
            player.resource.send(line.encode('utf-8'))


def finish(player):
    """
    Функция завершения игры
    """
    message = '\nСпасибо за игру\n'
    message += 'Ваш баланс составляет: {}\n'.format(player.money)
    player.resource.send(message.encode('utf8'))
    player.resource.close()


def make_bet(player):
    """
    Функция, обрабатывающая ставку игрока
    """
    while True:
        try:
            message = ('\nДелайте вашу ставку, минимальная '
                       'ставка 1$, у Вас сейчас {}$ '.format(player.money))
            player.resource.send(message.encode('utf8'))
            bet = float(player.resource.recv(64).decode('utf8'))
            if bet <= 0:
                playr.resource.send('Ваша ставка должна быть '
                                    'больше нуля.'.encode('utf8'))
            elif bet > player.money:
                player.resource.send('Вы не можете обеспечить '
                                     'данную ставку.'.encode('utf8'))
            else:
                break
        except ValueError:
            player.resource.send('\nВы должны ввести число.\n'.encode('utf8'))
    return bet


def move_interface(player):
    """
    Интерфейс хода игрока
    """
    while True:
        try:
            message = ('\nВыберите ваше действие, введите номер действия:\n'
                      ' 1. Взять дополнительную карту\n'
                      ' 2. Удвоить ставку\n'
                      ' 3. Завершить ход\n')
            player.resource.send(message.encode('utf8'))
            player.resource.send('Действие: '.encode('utf8'))
            action = int(player.resource.recv(64).decode('utf8').strip())
            if not 1 <= action <= 3:
                player.resource.send('Такого действия нет, '
                                     'попробуйте еще раз.\n\n'.encode('utf8'))
                continue
            break
        except ValueError:
            player.resource.send('Вы должны ввести число.\n\n'.encode('utf8'))
    return action


def start_game(player):
    """
    Интерфейс начала хода
    """
    while True:
        player.resource.send('\nГотовы ли Вы начать игру, д/н? '.encode('utf8'))
        action = player.resource.recv(5).decode('utf8')[:-1]
        if action == 'н':
            return False
        elif action == 'д':
            return True
        else:
            player.resource.send('У Вас всего два варианта: д - продолжить, '
                                 'н - завершить.\n\n'.encode('utf8'))


def player_info(player, message):
    """
    Вывод комнации карт у игрока или диллера и количества очков за нее
    """
    player.resource.send('\n{} карты:\n'.format(message).encode('utf8'))
    message = ' '.join(str(card) for card in player.cards) + '\n'
    player.resource.send(message.encode('utf8'))       
    if player.points == 21:
        ending = 'о'
    elif player.points % 10 <= 4 and (player.points < 10 or player.points > 20):
        ending = 'а'
    else:
        ending = 'ов'
    player.resource.send('Эта комбинация карт дает {} '
                         'очк{}.\n'.format(player.points, ending).encode('utf8'))


def print_message(player, message):
    """
    Небольшая вспомогательная функция
    """
    message += '\n'
    player.resource.send(message.encode('utf8'))
