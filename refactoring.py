import pygame
import random
import math
from numbers import Number

SCREEN_DIM = (800, 600)


class Vec2d:
    """Двумерный вектор, хотя это скорее точка"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec2d(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        # Скалярное умножение - скалярная величина, равная сумме попарного
        # произведения координат векторов
        if isinstance(other, Vec2d):
            return self.x*other.x + self.y+other.y
        elif isinstance(other, Number):
            return Vec2d(self.x*other, self.y*other)
        else:
            raise TypeError

    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    """
    Класс замкнутых ломаных
    """
    def __init__(self):
        self._points = []
        self._speeds = []

    def reset(self):
        self._points = []
        self._speeds = []

    def add_point(self, x, y):
        self._points.append(Vec2d(x, y))
        self._speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def draw_points(self, points=None, style="points", width=3,
                    color=(255, 255, 255)):
        """
        "Отрисовка" точек
        """
        if points is None:
            points = self._points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    def set_points(self):
        """
        Персчитывание координат опорных точек
        """
        for p in range(len(self._points)):
            self._points[p] = self._points[p] + self._speeds[p]
            if self._points[p].x > SCREEN_DIM[0] or self._points[p].x < 0:
                self._speeds[p] = Vec2d(-self._speeds[p].x, self._speeds[p].y)
            if self._points[p].y > SCREEN_DIM[1] or self._points[p].y < 0:
                self._speeds[p] = Vec2d(self._speeds[p].x, -self._speeds[p].y)


class Knot(Polyline):
    """
    Как я предполагаю - это класс петли
    """
    def __init__(self):
        super().__init__()
        self.count = 35

    def get_knot(self, color, style="line", width=3):
        if len(self._points) < 3:
            self.draw_points([], style, width, color)
            return
        res = []
        for i in range(-2, len(self._points) - 2):
            ptn = []
            ptn.append((self._points[i]+self._points[i + 1]) * 0.5)
            ptn.append(self._points[i + 1])
            ptn.append((self._points[i + 1]+self._points[i + 2]) * 0.5)
            res.extend(self._get_points(ptn))
        self.draw_points(res, style, width, color)

    def _get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg]*alpha +
                self._get_point(points, alpha, deg - 1)*(1 - alpha))


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(knot.count), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    working = True
    knot = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot.reset()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.count += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.count -= 1 if knot.count > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(*event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.get_knot(color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
