import requests
from bs4 import BeautifulSoup

from bot import Bot

bot = Bot()


@bot.on('message')
def title(parsed, user, target, text):
    if 'http://' in text or 'https://' in text:
        try:
            url = text[text.find('http'):].split()[0]
            response = requests.get(url, allow_redirects=True, timeout=2)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            title = title[:400] + '…' if len(title) > 400 else title
            bot.say(target, 'Title: {}'.format(title))
        except:
            pass
