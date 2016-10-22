import asyncio
from asyncirc import irc

import config


REGISTRY = dict()
bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
         .register(config.NICKNAME, config.NICKNAME, '{} (bot)'.format(config.NICKNAME))\
         .join(config.CHANNELS)


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
