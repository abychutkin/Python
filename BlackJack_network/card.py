class Card:
    """
    Класс игральной карты
    """
    def __init__(self, symbol):
        """
        При создании карты нужно указать одно обязательное значение:
        symbol - символ, представляющий собой изображение карты
        """
        self.symbol = symbol

    @property
    def value(self):
        """
        Свойство определения очков даваемых картой, определяется по последнему
        байту символа
        """
        card_value = (self.symbol.encode()[-1] - 129) % 16
        if 0 < card_value < 10:
            card_value += 1
        elif card_value >= 10:
            card_value = 10
        return card_value

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol
