import in_out


class BasePlayer:
    """
    Базовый класс игрока, от него наследуется игрок и диллер.
    При создании принимается необязательный параметр resource, он нужен в
    дальнейшем для расширения функционала, в дальнейшем в нем будет хранится
    сокет клиента. Также можно использовать что-то кроме сокета, если ввод/
    вывод будет осуществляться по другому, применяется в модуле in_out.
    """

    def __init__(self, resource=None):
        self.cards = []
        self.points = 0
        self.resource = resource

    def take_card(self, card):
        """
        Метод взятия карты и подсчет очков
        """
        self.cards.append(card)
        self._count_points(card.value)

    def return_cards(self):
        """
        Метод возврата карт в колоду и обнуление очков
        """
        cards_to_return = self.cards
        self.cards = []
        self.points = 0
        return cards_to_return

    def _count_points(self, card_points):
        """
        Метод подсчета очков от комбинации карт
        """
        if card_points == 0:
            # Определение стоимости туза
            if self.points+11 <= 21:
                self.points += 11
            else:
                self.points += 1
        else:
            self.points += card_points


class Dealer(BasePlayer):
    """
    Класс диллера
    """

    def make_move(self, card_deck):
        """
        Метод для проведения хода, карты берутся до тех пор пока не будет
        достигнуто 17 очков или более
        """
        while self.points < 17:
            self.take_card(card_deck.give_card())


class Player(BasePlayer):
    """
    Класс игрока
    """

    def __init__(self, resource=None):
        super().__init__(resource)
        self.money = 20.0
        # Изначально никакой ставки нет
        self.bet = None

    def make_move(self, card_deck):
        """
        Метод для проведения хода
        """
        # Здесь цикл добавлен, на случай если игрок удваивает, а денег у него
        # на это не хватает
        while True:
            action = in_out.move_interface(self)
            if action == 1:
                self.take_card(card_deck.give_card())
                in_out.player_info(self, 'Ваши')
            elif action == 2:
                if self.bet - self.money < 0.00000001:
                    self.money -= self.bet
                    self.bet *= 2
                    break
                else:
                    print('У Вас недостаточно денег для удвоения ставки\n')
                    continue
            elif action == 3:
                break

            if self.points >= 21:
                break

    def make_bet(self):
        """
        Данный метод позволяет игроку сделать ставку
        """
        self.bet = in_out.make_bet(self)
        self.money -= self.bet
