def my_range(*args):
    if len(args) < 1 or len(args) > 3:
        raise TypeError
    first = 0
    step = 1
    if len(args) == 1:
        last = args[0]
    elif len(args) >= 2:
        first = args[0]
        last = args[1]
        if len(args) == 3:
            step = args[2]
    while first < last:
        yield first
        first += step
