# Программа для демонстрации применения паттерна проектирования адаптер.
# Данная программа представляет расчет освещенности в игре с заранее
# определенными классами: Light и System, интерфейсы которых несовместимы.


class Light:
    def __init__(self, dim):
        """
        Класс Light создает поле заданного размера, представляющее собой
        карту на которой нужно расчитать освещение. За размер
        поля отвечает параметр, представляющий из себя кортеж из 2 чисел -
        dim. Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину.
        """
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        """
        Пересоздает поле
        """
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        """
        Метод устанавливает массив источников света с заданными
        координатами и просчитывает освещение.
        """
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        """
        Метод устанавливает препятствия. Положение элементов задается списком
        кортежей. В каждом элементе кортежа хранятся 2 значения: elem[0] -
        координата по ширине карты и elem[1] - координата по высоте
        соответственно.
        """
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        """
        Рассчитывает освещенность с учетом источников света и препятствий.
        По сути своей является имитацией так как просто возвращает
        созданное поле.
        """
        return self.grid.copy()


class System:
    """
    В системе в конструкторе создается двухмерная, карта, на которой источники
    света обозначены как 1, а препятствия как -1.
    """
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # источник света
        self.map[5][2] = -1  # стены

    def get_lightening(self, light_mapper):
        """
        Метод get_lightening принимает в качестве параметра объект, который
        должен просчитывать освещение. У объекта вызывается метод lighten,
        который принимает карту объектов и источников света и возвращает карту
        освещенности.
        """
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    """
    Адаптер для класса Light
    """
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        """
        Данный метод создает список источника света и препятствий
        """
        # Определение размеров карты
        grid_width = len(grid[0])
        grid_height = len(grid)

        # Изменения параметров адаптируемого объекта
        self.adaptee.set_dim((grid_width, grid_height))

        # Определение источников света и препятствий
        lights = []
        obstacles = []
        for i in range(grid_height):
            for j in range(grid_width):
                if grid[i][j] == 1:
                    lights.append((j, i))
                elif grid[i][j] == -1:
                    obstacles.append((j, i))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()
