import asyncio
from datetime import date, datetime
from dateutil import parser
import json

import bs4
import requests

from bot import Bot
from registry import bot_command
from storage import store


bot = Bot()


def _is_open():
    try:
        # response = requests.get('https://api.shack.space/v1/space')
        response = requests.get('http://localhost/v1/space')
        return json.loads(response.content.decode())['doorState']['open']
    except:
        return None


@bot_command('open')
def open(parsed, user, target, text):
    state = _is_open()
    if state is True:
        bot.say(target, 'shack is open')
    elif state is False:
        bot.say(target, 'shack is closed')
    else:
        bot.say(target, 'Defuq? I have no idea.')


@bot_command('plenum')
def next_plenum(parsed, user, target, text):
    try:
        response = requests.get('http://localhost/v1/plena/next')
        response.raise_for_status()
        # TODO HOW INTO ISODATE PARSING?
        next_date = parser.parse(json.loads(response.content.decode())['date'])
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
        response = requests.get('http://localhost/v1/plena/next')
        bot.say(target, json.loads(response.content.decode())['url'])
    except:
        bot.say(target, 'Plenum ist ja eigentlich auch überbewertet.')


@bot_command('online')
def online(parsed, user, target, text):
    try:
        response = requests.get('http://localhost/v1/online')
        bot.say(target, json.loads(response.content.decode())['message'])
    except:
        bot.say(target, 'rashfael: Das tut schon wieder nicht.')


def check_site():
    try:
        status = _is_open()
        if status is True:
            new = 'open'
        elif status is False:
            new = 'closed'
        else:
            new = 'no data'

        old = store.get('shack.state')
        old = old.decode() if old else ''

        if status is not None:
            store.set('shack.state', new)
            if 'open' in new and 'closed' in old:
                bot.say('#shackspace', 'The shack has been opened.')
            elif 'open' in old and 'closed' in new:
                bot.say('#shackspace', 'The shack has been closed.')
    except:
        pass

    asyncio.get_event_loop().call_later(60, check_site)


def check_blog():
    blog_key = 'shack.blogpost'
    response = requests.get('https://blog.shackspace.de/?feed=rss2')
    soup = bs4.BeautifulSoup(response.text, 'lxml-xml')
    latest_post = soup.rss.find('item')
    last_post = store.get(blog_key)
    last_post = last_post.decode() if last_post else ''
    store.set(blog_key, latest_post.link.text)

    if last_post != latest_post.link.text:
        bot.say('#shackspace', 'New blog post! »{title}« by {author}: {url}'.format(
            title=latest_post.title.text,
            author=latest_post.find('creator').text,
            url=latest_post.link.text,
        ))
    asyncio.get_event_loop().call_later(60, check_blog)


asyncio.get_event_loop().call_later(60, check_site)
asyncio.get_event_loop().call_later(60, check_blog)
