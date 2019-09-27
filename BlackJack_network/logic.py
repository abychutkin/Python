from players import Dealer, Player
from deck import CardDeck
import in_out


def game(player):
    """
    Данная функция управляет логикой игры, благодаря ней можно будет
    запускать несколько игр в разных потоках
    """
    in_out.rules(player)
    card_deck = CardDeck()
    dealer = Dealer(player.resource)
    while True:
        try:
            # Вначале игры все карты возвращаются в колоду, даже
            # в начале игры, когда карты не розданы это не повредит
            # это сделано чтобы излишне не усложнять код
            card_deck.take_cards(player.return_cards())
            card_deck.take_cards(dealer.return_cards())

            card_deck.shuffle()

            # Переменные указывающие на наличие комбинации Блекджек у игрока
            # и диллера
            player_blackjack = False
            dealer_blackjack = False

            # Определить, есть ли деньги у игрока, если нет, то игра завершена
            # Также уточняется хочет ли пользователь играть
            if player.money < 1 or not in_out.start_game(player):
                in_out.finish(player)

            # Предложить сделать ставку, указав, что минимальная ставка
            # 1 доллар
            player.make_bet()
            # Сдается две карты игроку
            for _ in range(2):
                player.take_card(card_deck.give_card())
            # Сдается одна карта дилеру
            dealer.take_card(card_deck.give_card())
            # Показываются карты дилера
            in_out.player_info(dealer, 'Диллера')
            # Показываются карты игрока
            in_out.player_info(player, 'Ваши')
            # Если у игрока блекджек (на руках две карты, количество очков -
            # 21), то задается соответствующая переменная, иначе берется карта
            if player.points != 21:
                player.make_move(card_deck)
            else:
                player_blackjack = True
            # Проверка наличия блекджека у диллера
            dealer.take_card(card_deck.give_card())
            if dealer.points != 21:
                dealer.make_move(card_deck)
            else:
                dealer_blackjack = True

            # Если у пользователя на руках блекджек и у диллера блекджека нет,
            # то пользователь выигрывает 3 к 1
            if player_blackjack and not dealer_blackjack:
                player.money += player.bet * 2.5
                in_out.print_message(player, 'Вы выиграли {:} $\
                                             \n'.format(round(player.bet*1.5, 2)))
                continue

            if player.points > 21:
                in_out.print_message(player, 'Вы проиграли, сожалеем.\n')
                continue

            in_out.player_info(dealer, 'Диллера')

            if player.points < dealer.points and dealer.points <= 21:
                in_out.print_message(player, 'Вы проиграли, сожалеем.\n')
            elif player.points > dealer.points or dealer.points > 21:
                player.money += player.bet * 2.0
                in_out.print_message(player, 'Вы выиграли {:} $\
                                      \n'.format(round(player.bet, 2)))
            else:
                player.money += player.bet
                in_out.print_message(player, 'Вы сыграли в ничью\n')
        except KeyboardInterrupt:
            in_out.finish(player)


if __name__ == '__main__':
    player = Player()
    game(player)
