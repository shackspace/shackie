from asyncirc import irc

import config


class Bot:
    bot = None

    def __new__(cls, *args, **kwargs):
        if not cls.bot:
            password = None
            if 'PASSWORD' in dir(config):
                password = config.PASSWORD
            cls.bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
                .register(config.NICKNAME, config.NICKNAME, '{} (bot)'.format(config.NICKNAME), password=password)\
                .join(config.CHANNELS)
        return cls.bot
