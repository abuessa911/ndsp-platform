ENGINES = {}

def register(name):
    def wrapper(func):
        ENGINES[name] = func
        return func
    return wrapper

def get_engines():
    return ENGINES
