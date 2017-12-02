import aiohttp
import asyncio
import async_timeout
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


async def _is_open():
    try:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            with async_timeout.timeout(5):
                async with session.get('http://api.shackspace.de/v1/space') as resp:
                    return json.loads(await resp.text())['doorState']['open']
    except:
        return None


@bot_command('open')
async def open(parsed, user, target, text):
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
    state = await _is_open()
    if state is True:
        bot.say(target, random.choice(open_choices))
    elif state is False:
        bot.say(target, random.choice(closed_choices))
    else:
        bot.say(target, random.choice(defuq_choices))


@bot_command('plenum')
async def next_plenum(parsed, user, target, text):
    try:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            with async_timeout.timeout(5):
                async with session.get('http://api.shackspace.de/v1/plena/next') as resp:
                    next_date = parser.parse(json.loads(await resp.text())['date'])
                    delta = (next_date.date() - date.today()).days

                    if delta == 0:
                        reply_string = "Heute um 20 Uhr ist Plenum!"
                    elif delta == 1:
                        reply_string = "Morgen um 20 Uhr ist Plenum!"
                    else:
                        reply_string = "Das nächste Plenum ist in {delta} Tagen, am {date}, um 20 Uhr.".format(
                            delta=delta, date=next_date.strftime('%d.%m')
                        )
                    bot.say(target, reply_string)

    except:
        bot.say(target, 'Heute Plenum, morgen Plenum, das sind doch bürgerliche Kategorien.')


@bot_command(['plenumlink', 'plenumslink'])
async def link_plenum(parsed, user, target, text):
    try:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            with async_timeout.timeout(5):
                async with session.get('http://api.shackspace.de/v1/plena/next') as resp:
                    bot.say(target, json.loads(await resp.text())['url'])
    except:
        bot.say(target, 'Plenum ist ja eigentlich auch überbewertet.')


@bot_command('online')
async def online(parsed, user, target, text):
    try:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            with async_timeout.timeout(5):
                async with session.get('http://api.shackspace.de/v1/online') as resp:
                    bot.say(target, json.loads(await resp.text())['message'])
    except:
        bot.say(target, 'rashfael: Das tut schon wieder nicht.')


async def check_site():
    while True:
        await asyncio.sleep(60)
        status = await _is_open()
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


async def check_blog():
    blog_key = 'shack.blogpost'
    while True:
        await asyncio.sleep(60)
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(30):
                    async with session.get('http://blog.shackspace.de/?feed=rss2') as resp:
                        soup = bs4.BeautifulSoup(await resp.text(), 'lxml-xml')
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
        except (asyncio.CancelledError, asyncio.TimeoutError):
            print('timeout')


def is_valid_change(latest_change):
    forbidden_values = ['spielwiese', 'friedhof']
    return not any([value in latest_change['title'] for value in forbidden_values])


async def check_wiki():
    wiki_key = 'shack.wikichange'
    while True:
        await asyncio.sleep(60)
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(30):
                    async with session.get('http://wiki.shackspace.de/feed.php') as resp:
                        feed = feedparser.parse(await resp.text())
                        latest_change = feed.entries[0]

                        last_change = store.get(wiki_key)
                        last_change = last_change.decode() if last_change else ''
                        store.set(wiki_key, latest_change['id'])

                        if last_change != latest_change['id'] and is_valid_change(latest_change):
                            response = 'Page changed: ' + latest_change['title']
                            response += ' by ' + latest_change['authors'][0]['name'] if latest_change.get('authors') else ''
                            response += ' – ' + latest_change['links'][0]['href']
                            bot.say('#shackspace', response)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            print('timeout')


asyncio.ensure_future(check_site())
asyncio.ensure_future(check_blog())
asyncio.ensure_future(check_wiki())
