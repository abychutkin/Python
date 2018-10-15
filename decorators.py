# Наиболее простой декоратор
def simple_decorator(func):
    def wrapper():
        print("Executing code before function")
        func()
        print("Executing code after function")
    return wrapper


@simple_decorator
def simple_function():
    print("Executing function")

# Данный декоратор передает аргументы в функцию, которую оборачивает
def decorator_gives_args_to_func(func):
    def wrapper(*args, **kwargs):
        print("Positional arguments:", args)
        print("Keyword arguments:", kwargs)
        func(*args, **kwargs)
    return wrapper


# Декоратор, который может принимать параметры, для чего используется промежуточная функция
def decorator_creator(creator_name):
    print("Выполняется промежуточная функция один раз, получая аргументы, ")
    print("которые будут использованы для создания декоратора")
    print("Данная функция приняла один аргумент:", creator_name)
    def decorator(func):
        print("Данная функция создает декоратор и тоже выполняется один раз при его создании")
        def wrapper(*args, **kwargs):
            print("Данная функция будет выполняться каждый раз при вызове декорированной функции и создана она {}".format(creator_name))
            print("Принятые аргументы:", args, **kwargs)
            func(*args, **kwargs)
        return wrapper
    return decorator


@decorator_gives_args_to_func
def function_with_args(*args, **kwargs):
    print("Here goes positional args:")
    for arg in args:
        print(arg)
    print("Here goes keyword args:")
    for key, value in kwargs.items():
        print("{} associated with {}".format(key, value))

@decorator_creator("Aleksey")
def adding(a, b):
    print(a + b)


simple_function()
function_with_args(1, 2, 3, 4, 5, first=1, second=2)
adding(4, 5)
adding(7, 8)
