import asyncio
from asyncirc import irc

bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
         .register("NICKNAME", "shackbot", "shackbot")\
         .join("#shackspace-dev")


@bot.on("message")
def incoming_message(parsed, user, target, text):
    bot.say(target, "{}: you said {}".format(user.nick, text))


@bot.on("join")
def on_join(message, user, channel):
    bot.say(channel, "Hi {}! You're connecting from {}.".format(user.nick, user.host))


asyncio.get_event_loop().run_forever()
