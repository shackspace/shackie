import requests
from datetime import date, datetime

from bot import Bot
from registry import bot_command


bot = Bot()


@bot_command('open')
def open(parsed, user, target, text):
    try:
        response = requests.get('http://shackspace.de/sopen/text/en')
        response.raise_for_status()
        reply = response.content.decode()
    except:
        bot.say(target, 'Error ({}) while trying to reach the shack :('.format(
            response.status_code if response else 'ouch!')
        )
    else:
        if 'open' in reply:
            bot.say(target, 'shack is open')
        elif 'close' in reply:
            bot.say(target, 'shack is closed')
        else:
            bot.say(target, 'Defuq? I have no idea.')
