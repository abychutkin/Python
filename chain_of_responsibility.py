# Программа для демонстрации паттерна цепочка обязанностей
# В данной программа необходимо реализовать: EventGet(<type>) - создает событие
# получения данных соответствующего типа; EventSet(<value>) - создает событие
# изменения поля типа type(<value>)
#
# Необходимо реализовать классы NullHandler, IntHandler, FloatHandler,
# StrHandler так, чтобы можно было создать цепочку:
# chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
#
# chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
# chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
# chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
# chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
# chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
# chain.handle(obj, EventSet("str")) — установить значение
# obj.string_field = "str"


class SomeObject:
    """
    Объект, объявленный преподаветалями для хранения данных
    """
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class BaseEvent:
    """
    Базовый класс события
    """
    def __init__(self, value):
        self.event_value = value
        self.event_type = self.get_event_type()

    def get_event_type(self):
        """
        Метод определяет тип события
        """
        return self.__class__.__name__[-3:]


class EventGet(BaseEvent):
    """
    Событие по сути нужно для его имени
    """
    pass


class EventSet(BaseEvent):
    """
    Событие по сути нужно для его имени
    """
    pass


class NullHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, obj, event):
        if self._next_handler is not None:
            return self._next_handler.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.event_type == 'Get' and event.event_value == int:
            return obj.integer_field
        elif event.event_type == 'Set' and isinstance(event.event_value, int):
            obj.integer_field = event.event_value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.event_type == 'Get' and event.event_value == float:
            return obj.float_field
        elif event.event_type == 'Set' and isinstance(event.event_value, float):
            obj.float_field = event.event_value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.event_type == 'Get' and event.event_value == str:
            return obj.string_field
        elif event.event_type == 'Set' and isinstance(event.event_value, str):
            obj.string_field = event.event_value
        else:
            return super().handle(obj, event)
