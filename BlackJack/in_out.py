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
            print(line)


def finish(player):
    """
    Функция завершения игры
    """
    print('\nСпасибо за игру')
    print('Ваш баланс составляет:', player.money)
    exit()


def make_bet(player):
    """
    Функция, обрабатывающая ставку игрока
    """
    while True:
        try:
            bet = float(input('Делайте вашу ставку, минимальная ставка 1$, '
                              'у Вас сейчас {}$ '.format(player.money)))
            if bet <= 0:
                print('Ваша ставка должна быть больше нуля.')
            elif bet > player.money:
                print('Вы не можете обеспечить данную ставку.')
            else:
                break
        except ValueError:
            print('Вы должны ввести число.')
    return bet


def move_interface(player):
    """
    Интерфейс хода игрока
    """
    while True:
        try:
            print('Выберите ваше действие, введите номер действия:')
            print(' 1. Взять дополнительную карту')
            print(' 2. Удвоить ставку')
            print(' 3. Завершить ход')
            action = int(input('Действие: '))
            if not 1 <= action <= 3:
                print('Такого действия нет, попробуйте еще раз.\n')
                continue
            break
        except ValueError:
            print('Вы должны ввести число.\n')
    print()
    return action


def start_game(player):
    """
    Интерфейс начала хода
    """
    while True:
        action = input('Готовы ли Вы начать игру, д/н? ')
        if action == 'д':
            action = True
        elif action == 'н':
            action = False
        else:
            print('У Вас всего два варианта: д - продолжить, н - завершить.\n')
            continue
        break
    print()
    return action


def player_info(player, message):
    """
    Вывод комнации карт у игрока или диллера и количества очков за нее
    """
    print("{} карты:".format(message))
    for card in player.cards:
        print(card, end=' ')
    print()
    if player.points == 21:
        ending = 'о'
    elif player.points % 10 <= 4 and (player.points < 10 or player.points > 20):
        ending = 'а'
    else:
        ending = 'ов'
    print("Эта комбинация карт дает {} очк{}.".format(player.points, ending))
    print()


def print_message(player, message):
    """
    Небольшая вспомогательная функция
    """
    print(message)
