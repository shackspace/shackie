REGISTRY = dict()


def _bot_command(func, name):
    def ret_fun(*args, **kwargs):
        return func(*args, **kwargs)

    def update_registry(key, value):
        if key in REGISTRY:
            raise Exception('Command {} is already defined.'.format(key))
        REGISTRY[key] = value

    if not name:
        name = func.__name__

    if isinstance(name, list):
        for n in name:
            update_registry(n, func)
    else:
        update_registry(name, func)
    return ret_fun


def bot_command(name):
    def wrap(f):
        return _bot_command(f, name)
    return wrap
