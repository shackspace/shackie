from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup

from bot import Bot
from storage import store

from config import IGNORE

bot = Bot()


def _handle_title(url, bot, target):
    try:
        domain = "{0.netloc}".format(urlsplit(url))

        response = requests.get(url, allow_redirects=True, timeout=2)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip()

        if title:
            title = title.split('\n')[0]
            title = title[:400] + '…' if len(title) > 400 else title
            bot.say(target, 'Title: {title} (at {domain})'.format(title=title, domain=domain))
    except:
        pass


def _handle_repeat(url, bot, target):
    bare_url = '{0.netloc}{0.path}?{0.query}'.format(urlsplit(url))
    redis_string = 'urls.{}§{}'.format(target, bare_url)
    count = int(store.get(redis_string) or 0)

    if count:
        if count == 1:
            message = 'This url has been posted already, lame!'
        elif count == 2:
            message = 'This url has been posted twice before, must be important.'
        else:
            message = 'This url has been posted {} times before.'.format(count)
        bot.say(target, message)
        store.incr(redis_string, 1)
    else:
        store.set(redis_string, 1)


@bot.on('message')
def title(parsed, user, target, text):
    if user.nick in IGNORE : return
    if 'http://' in text or 'https://' in text:
        url = text[text.find('http'):].split()[0]
        _handle_title(url, bot, target)
        _handle_repeat(url, bot, target)
