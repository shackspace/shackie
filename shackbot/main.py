import asyncio
from asyncirc import irc

import config


REGISTRY = dict()
bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
         .register(config.NICKNAME, config.NICKNAME, '{} (bot)'.format(config.NICKNAME))\
         .join(config.CHANNELS)


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


@bot_command(['other_name_for_command', 'beispiel'])
def example(parsed, user, target, text):
    print('Called example function')


@bot.on("message")
def incoming_message(parsed, user, target, text):
    if text.startswith('.status'):
        bot.say(target, "everything is ok, {}".format(user.nick))


@bot.on("message")
def bot_message(parsed, user, target, text):
    if text.startswith(config.BOT_CHAR):
        command = text.split()[0]
        if len(command) > 1:
            command = command[1:]
            if command in REGISTRY:
                REGISTRY[command](parsed, user, target, text)
            elif config.SAY_NO:
                bot.say(target, 'I don\'t know what {} means.'.format(command))


asyncio.get_event_loop().run_forever()
