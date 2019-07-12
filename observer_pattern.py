# Программа для демонстрации паттерна наблюдатель. В данной программе
# реализовано получение достижений в игре. Предполагается что есть
# класс Engine, который представляет собой движок игры, и может создавать
# уведомления о достижениях, создание движка не предполагается.
#
# Необходимо создать класс обертку над движком, которая будет иметь
# возможность подписывать наблюдателей и рассылать им уведомления, а также
# иерархию наблюдателей.
#
# Пример достижения - {"title": "Покоритель",
#                      "text": "Дается при выполнении всех заданий в игре"}


from abc import ABC, abstractmethod


# Объявления класса исключительно для дебага
class Engine:
    pass


class ObservableEngine(Engine):
    """
    Класс обертка для движка игры
    """
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        """
        Метод подписывает наблюдателя для слежения за обновлениями
        """
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        """
        Метод отписывает заданного подписчика
        """
        self.__subscribers.discard(subscriber)

    def notify(self, achievement):
        """
        Уведомляет всех подписчиков о получении достижения
        """
        for subscriber in self.__subscribers:
            subscriber.update(achievement)


class AbstractObserver(ABC):
    """
    Абстрактный наблюдатель, являющийся родителем для всех прочих наблюдателей
    """
    @abstractmethod
    def update(self, achievement):
        """
        Абстрактный метод, который необходимо переопределить в потомках
        """
        pass


class ShortNotificationPrinter(AbstractObserver):
    """
    Класс наблюдатель содержащий в себе только названия полученных достижений
    """
    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        """
        Метод обновления перечня достижений
        """
        self.achievements.add(achievement['title'])


class FullNotificationPrinter(AbstractObserver):
    """
    Класс наблюдатель, содержащий в себе расширенный список достижений
    """
    def __init__(self):
        self.achievements = []

    def update(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
