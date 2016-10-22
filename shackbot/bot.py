from asyncirc import irc

import config


class Bot:
    bot = None
    def __new__(cls, *args, **kwargs):
        if not cls.bot:
            cls.bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
                .register(config.NICKNAME, config.NICKNAME, '{} (bot)'.format(config.NICKNAME))\
                .join(config.CHANNELS)
        return cls.bot
