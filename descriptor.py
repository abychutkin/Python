# В данной программе релизован дескриптор,
# который корректирует сумму на
# коэффициент, содержащийся в
# вызывающем его объекте


class Value:

    def __init__(self):
        self.amount = None

    def __get__(self, obj, obj_type):
        # Тут просто в образовательных целях реализовано,
        # что при обращении от класса, будет возвращаться
        # строка с описанием аттрибута.
        # При обращении от класса obj == None
        if obj:
            return self.amount
        return 'Аттрибут для хранения итоговой суммы'

    def __set__(self, obj, value):
        self.amount = round(value * (1 - obj.commission))
