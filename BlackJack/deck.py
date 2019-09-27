import random
from symbols_generator import symbols_generator
from card import Card


class CardDeck:
    """
    Класс представляет собой колоду, состоящую из 52 карт
    """
    def __init__(self):
        self.__cards = []
        for symbol in symbols_generator():
            self.__cards.append(Card(symbol))

    def shuffle(self):
        """
        Тасование колоды
        """
        random.shuffle(self.__cards)

    def give_card(self):
        """
        Метод сдачи карты
        """
        return self.__cards.pop(0)

    def take_cards(self, cards):
        """
        Возврат карт в колоду
        """
        self.__cards.extend(cards)
