REGISTRY = dict()


def _bot_command(func, name):
    def ret_fun(*args, **kwargs):
        return func(*args, **kwargs)
    if not name:
        name = func.__name__

    if isinstance(name, list):
        REGISTRY.update({n: func for n in name})
    else:
        REGISTRY[name] = func
    return ret_fun


def bot_command(name):
    def wrap(f):
        return _bot_command(f, name)
    return wrap
