import asyncio
from asyncirc import irc

import config


bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
         .register(config.NICKNAME, config.NICKNAME, ' (bot)'.format(config.NICKNAME))\
         .join(config.CHANNELS)


@bot.on("message")
def incoming_message(parsed, user, target, text):
    if text.startswith('.status'):
        bot.say(target, "everything is ok, {}".format(user.nick))


asyncio.get_event_loop().run_forever()
