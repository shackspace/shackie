import asyncio
import requests
from datetime import date, datetime

from bot import Bot
from registry import bot_command
from storage import store


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


@bot_command('plenum')
def next_plenum(parsed, user, target, text):
    try:
        response = requests.get('http://shackspace.de/nextplenum/text/iso')
        response.raise_for_status()
        next_date = datetime.strptime(response.content.decode().strip(), '%Y-%m-%d')
        delta = (next_date.date() - date.today()).days

        if delta == 0:
            reply_string = "Heute ist Plenum!"
        elif delta == 1:
            reply_string = "Morgen ist Plenum!"
        else:
            reply_string = "Das nächste Plenum ist in {delta} Tagen, am {date}.".format(
                delta=delta, date=next_date.strftime('%d.%m')
            )
        bot.say(target, reply_string)
    except:
        bot.say(target, 'Heute Plenum, morgen Plenum, das sind doch bürgerliche Kategorien.')


@bot_command(['plenumlink', 'plenumslink'])
def link_plenum(parsed, user, target, text):
    try:
        bot.say(target, requests.get('http://shackspace.de/nextplenum/http300/current').url)
    except:
        bot.say(target, 'Plenum ist ja eigentlich auch überbewertet.')


@bot_command('online')
def online(parsed, user, target, text):
    try:
        bot.say(target, requests.get('http://shackproxy.unimatrix21.org/shackles/online').content.decode())
    except:
        bot.say(target, 'rashfael: Das tut schon wieder nicht.')


def check_site():
    try:
        response = requests.get('http://shackspace.de/sopen/text/en')
        response.raise_for_status()
        new = response.content.decode().strip()
        old = store.get('shack.state').decode() or ''
        store.set('shack.state', new)

        if old and (old != new):
            bot.say('#shackspace-dev', 'shack switched from {} to {}.'.format(old, new))
    except:
        pass

    asyncio.get_event_loop().call_later(60, check_site)

asyncio.get_event_loop().call_later(60, check_site)
