def calculate(data, findall):
    """Функция для расчета арифметических выражений и изменения
    значения переменных полученных в словаре data, принимает
    функцию в которой определенны данные для поиска.
    Арифметические выражения упрощенные: есть только 3 переменные и
    две операции - сложение и вычитание."""
    matches = findall(r"([abc])([+-]?)=([abc]?)([+-]?\d*)")
    for var1, sign, var2, number in matches:
        right_side = data.get(var2, 0) + int(number or 0)
        if sign == '+':
            data[var1] += right_side
        elif sign == '-':
            data[var1] -= right_side
        else:
            data[var1] = right_side
    return data
