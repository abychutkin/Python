from bs4 import BeautifulSoup
from collections import deque
import re
import os


def build_tree(start, end, path):
    """Функция реализует поиск в ширину по графу, она работает по заданной
    директории, и находит путь от start до end, предполагается что существует
    только один кратчайший путь. Формирует словарь в котором странице
    проставлен родитель, начиная от start и завершая end."""
    # Регулярное выражение, предоставлено преподавателями
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")
    files = dict.fromkeys(os.listdir(path))
    links_to_visit = deque([start])
    visited_links = set()
    while links_to_visit:
        current_link = links_to_visit.popleft()
        visited_links.add(current_link)
        with open('{}{}'.format(path, current_link)) as data:
            links = link_re.findall(data.read())
            for link in links:
                if link in files:
                    if not files[link]:
                        files[link] = current_link
                    if link not in visited_links:
                        links_to_visit.append(link)
                    if link == end:
                        return files


def build_bridge(start, end, path):
    """Формирует последовательность страниц начиная от start до
    finish. Стоит отметить то, что хотя данная последовательность
    является развернутой, но это никак не влияет на их анализ."""
    files = build_tree(start, end, path)
    bridge = []
    while end != start:
        bridge.append(end)
        end = files[end]
    bridge.append(start)
    return bridge


def count_images(page):
    """Функция для подсчета изображений, шириной больше 200."""
    result = 0
    for image in page.find_all('img', width=True):
        if int(image['width']) >= 200:
            result += 1
    return result


def count_headers(page):
    """Функция подсчитывает заголовки, начинающиеся с заданных букв"""
    result = 0
    headers = ['h'+str(i) for i in range(1, 7)]
    letters = 'ETC'
    for header in headers:
        tags = page.find_all(header)
        for tag in tags:
            if tag.text[0] in letters:
                result += 1
    return result


def count_consecutive_links(page):
    """Функция определяет длину наибольшей последовательности ссылок."""
    result = 0
    links = page.find_all('a')
    for link in links:
        consecutive_links = 1
        next_link = link.findNextSibling()
        while next_link and next_link.name == 'a':
            consecutive_links += 1
            link = next_link
            next_link = link.findNextSibling()
        if consecutive_links >= result:
            result = consecutive_links
    return result


def count_outer_lists(page):
    """Функция считает количество невложенных списков"""
    result = 0
    lists = page.find_all('ol')
    lists.extend(page.find_all('ul'))
    for list_ in lists:
        list_parents = list_.parents
        for parent in list_parents:
            if parent.name == 'li':
                break
        else:
            result += 1
    return result


def parse(start, end, path):
    """
    Функция для анализа перечня страниц
    """

    bridge = build_bridge(start, end, path)

    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        # Данные извлекаются из определенной части страниц
        body = soup.find(id="bodyContent")

        imgs = count_images(body)
        headers = count_headers(body)
        linkslen = count_consecutive_links(body)
        lists = count_outer_lists(body)

        out[file] = [imgs, headers, linkslen, lists]

    return out
