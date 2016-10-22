import asyncio
from asyncirc import irc

bot = irc.connect("chat.freenode.net", 6667, use_ssl=False)\
         .register("NICKNAME", "shackbot", "shackbot")\
         .join("#shackspace-dev")


@bot.on("message")
def incoming_message(parsed, user, target, text):
    if text.startswith('.status'):
        bot.say(target, "everything is ok, {}".format(user.nick))


asyncio.get_event_loop().run_forever()
