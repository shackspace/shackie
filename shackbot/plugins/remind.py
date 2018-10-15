import asyncio
import datetime
import math
import pytz

from bot import Bot
from copy import copy
from functools import partial
from config import IGNORE
from registry import bot_command


@bot_command('remind')
def remind(parsed, user, target, text):
    if user.nick in IGNORE:
        return
    bot = Bot()

    def startmsg(target, user, seconds, message):
        minutes = math.floor(seconds / 60)
        pl = 's' if minutes != 1 else ''
        m = "Reminding {} in {} minute{}: {}".format(user.nick, minutes,
                                                     pl, message)
        bot.say(target, m)

    def f(bot, user, target, message):
        m = "%s: --- %s ---" % (user.nick, message)
        bot.say(target, m)

    message = None
    seconds = None

    sp = text.split()
    timevalue = sp[0]

    if str(timevalue).isdigit():
        seconds = int(timevalue) * 60
    else:
        if ':' not in timevalue:
            timevalue = sp[1]
            if ':' in timevalue or str(timevalue).isdigit():
                if str(timevalue).isdigit():
                    seconds = int(timevalue) * 60
                # <user> <time> <message>
                timevalue = sp[1]
                message = " ".join(sp[2:])
        if not seconds:
            try:
                tm = [int(i) for i in timevalue.split(':')]
                berlin = pytz.timezone('Europe/Berlin')
                now = pytz.utc.localize(datetime.datetime.now())
                x = berlin.localize(datetime.datetime.now())
                x = x.replace(hour=tm[0], minute=tm[1])
                # calculate datetimedelta and save difference in seconds
                seconds = (x - now).seconds
            except:
                seconds = None

    if not message:
        message = " ".join(sp[1:])

    if seconds:
        asyncio.get_event_loop().call_later(seconds, partial(f, bot, user, target, message))
        startmsg(target, user, seconds, message)
    else:
        bot.say(target, '.remind [minutes/time] [message]')

