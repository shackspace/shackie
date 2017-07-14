import asyncio
from datetime import date, datetime
from dateutil import parser
import json
import random

import bs4
import feedparser
import requests

from bot import Bot
from registry import bot_command
from storage import store


bot = Bot()


def _is_open():
    try:
        # response = requests.get('https://api.shack.space/v1/space')
        response = requests.get('http://localhost/v1/space', timeout=5)
        return json.loads(response.content.decode())['doorState']['open']
    except:
        return None


@bot_command('open')
def open(parsed, user, target, text):
    defuq_choices = [
        'Defuq? I have no idea.',
        'Can\'t reach the space, it probably burned down ...',
        'I could tell you, but then I\'d have to kill you.',
        'You know, a hackerspace is supposed to be made up of technologically capable people. So why is your infrastructure down again?',
    ]
    open_choices = [
        'shack is open.',
        'Your favourite hackerspace is open.',
        'It\'s open.',
        'Happy hacking, the shackspace is open.',
        'open.',
        'offen.',
        'åpen',
        'öppen',
    ]
    closed_choices = [
        'shack is closed.',
        'Your favourite hackerspace is closed.',
        'It\'s closed.',
        'Can\'t hack at shackspace, the shackspace is closed.',
        'shackspace is closed, hack the system instead.',
        'closed.',
        'zu.',
        'geschlossen.',
    ]
    state = _is_open()
    if state is True:
        bot.say(target, random.choice(open_choices))
    elif state is False:
        bot.say(target, random.choice(closed_choices))
    else:
        bot.say(target, random.choice(defuq_choices))


@bot_command('plenum')
def next_plenum(parsed, user, target, text):
    try:
        response = requests.get('http://localhost/v1/plena/next', timeout=5)
        response.raise_for_status()
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
        response = requests.get('http://localhost/v1/plena/next', timeout=5)
        bot.say(target, json.loads(response.content.decode())['url'])
    except:
        bot.say(target, 'Plenum ist ja eigentlich auch überbewertet.')


@bot_command('online')
def online(parsed, user, target, text):
    try:
        response = requests.get('http://localhost/v1/online', timeout=10)
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
    response = requests.get('http://blog.shackspace.de/?feed=rss2', timeout=15)
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


def check_wiki():
    wiki_key = 'shack.wikichange'
    feed = feedparser.parse('http://wiki.shackspace.de/feed.php')
    latest_change = feed.entries[0]

    last_change = store.get(wiki_key)
    last_change = last_change.decode() if last_change else ''
    store.set(wiki_key, latest_change['id'])

    if last_change != latest_change['id']:
        response = 'Page changed: ' + latest_change['title']
        response += ' by ' + latest_change['authors'][0]['name'] if latest_change.get('authors') else ''
        response += ' – ' + latest_change['links'][0]['href']
        bot.say('#shackspace', response)
    asyncio.get_event_loop().call_later(60, check_wiki)


asyncio.get_event_loop().call_later(60, check_site)
asyncio.get_event_loop().call_later(60, check_blog)
asyncio.get_event_loop().call_later(60, check_wiki)
