# Пример реализации паттерна декоратор.


from abc import ABC, abstractmethod


class Hero:
    """
    Класс героя, у которого есть основные характеристики и он может
    получать различные баффы, которые увеличивают некоторые
    характеристики, и дебаффы, которые снижают некоторые характеристики.
    Эффект одинаковых баффов и дебаффов суммируется. Игрок может
    получать перечень дебаффов и баффов, наложенных на него.
    """
    def __init__(self):
        self.__positive_effects = []
        self.__negative_effects = []
        self.__stats = {
             "HP": 128,
             "MP": 42,
             "SP": 100,
             "Strength": 15,
             "Perception": 4,
             "Endurance": 8,
             "Charisma": 2,
             "Intelligence": 3,
             "Agility": 8,
             "Luck": 1
        }

    def get_positive_effects(self):
        """
        Метод возвращает перечень баффов, наложенных на героя.
        """
        return self.__positive_effects.copy()

    def get_negative_effects(self):
        """
        Метод возвращает перечень дебаффов, наложенных на героя.
        """
        return self.__negative_effects.copy()

    def get_stats(self):
        """
        Метод возращает характеристики героя.
        """
        return self.__stats.copy()


class AbstractEffect(Hero, ABC):
    """
    Базовый абстрактный декоратор, от которого будут наследовать
    декораторы AbstractNegative и AbstractPositive.
    Данный класс наследует от Hero только потому что так требует
    задание.
    """
    def __init__(self, base):
        self.base = base
        # В данной переменной будет сохранятся изменение в статах,
        # произошедшие из-за баффа или дебаффа
        self._new_stats = {}

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_stats(self):
        """
        Метод при вызове возвращает динамически измененные характеристики
        героя
        """
        result = self.base.get_stats()
        for key in self._new_stats:
            result[key] += self._new_stats[key]
        return result


class AbstractPositive(AbstractEffect):
    """
    Абстрактный декоратор, являющийся базовым для всех
    баффов
    """
    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Berserk(AbstractPositive):
    """
    Декоратор Берсерк.
    Увеличивает параметры Сила, Выносливость, Ловкость, Удача на 7;
    уменьшает параметры Восприятие, Харизма, Интеллект на 3.
    Количество единиц здоровья увеличивается на 50.
    """
    def __init__(self, base):
        super().__init__(base)
        self._new_stats = {"Strength": 7, "Endurance": 7, "Agility": 7,
                           "Luck": 7, "Perception": -3, "Charisma": -3,
                           "Intelligence": -3, "HP": 50}

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Berserk"]


class Blessing(AbstractPositive):
    """
    Декоратор Благословения.
    Увеличивает все основные параметры на 2.
    Частично компенсирует уменьшение характеристик от Берсерка.
    """
    def __init__(self, base):
        super().__init__(base)
        self._new_stats = {"Strength": 2, "Endurance": 2, "Agility": 2,
                           "Luck": 2, "Perception": 2, "Charisma": 2,
                           "Intelligence": 2}

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Blessing"]


class AbstractNegative(AbstractEffect):
    """
    Абстрактный декоратор, являющийся базовым для всех
    дебаффов
    """
    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Weakness(AbstractNegative):
    """
    Декоратор Слабости.
    Уменьшает параметры Сила, Выносливость, Ловкость на 4
    """
    def __init__(self, base):
        super().__init__(base)
        self._new_stats = {"Strength": -4, "Endurance": -4, "Agility": -4}

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Weakness"]


class EvilEye(AbstractNegative):
    """
    Декоратор Сглаз.
    Уменьшает параметр Удача на 10
    """
    def __init__(self, base):
        super().__init__(base)
        self._new_stats = {"Luck": -10}

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["EvilEye"]


class Curse(AbstractNegative):
    """
    Декоратор Проклятья.
    Уменьшает все основные характеристики на 2.
    """
    def __init__(self, base):
        super().__init__(base)
        self._new_stats = {"Strength": -2, "Endurance": -2, "Agility": -2,
                           "Luck": -2, "Perception": -2, "Charisma": -2,
                           "Intelligence": -2}

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Curse"]
