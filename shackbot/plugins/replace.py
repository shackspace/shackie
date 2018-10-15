"""
via http://cgit.cd.krebsco.de/stockholm/tree/krebs/5pkgs/Reaktor/scripts/sed-plugin.py
"""
import re
from subprocess import Popen, PIPE

from bot import Bot
from config import IGNORE
from storage import store


bot = Bot()


def is_replace(line):
    myre = re.compile(r'^s/(?:\\/|[^/])+/(?:\\/|[^/])*/[ig]?$')
    return myre.match(line)


@bot.on('message')
def replace_entrypoint(parsed, user, target, text):
    if user.nick in IGNORE:
        return
    if is_replace(text):
        last_line = store.get('replace.{}.{}'.format(target, user.nick)).decode()
        if last_line:
            proc = Popen(
                ['sed', text],
                stdin=PIPE, stdout=PIPE
            )
            out, error = proc.communicate(bytes("{}\n".format(last_line), "UTF-8"))
            if proc.returncode:
                bot.say(target, "Something went wrong when trying to process your regex: {}".format(error.decode()))
                return

            result = out.decode()
            bot.say(target, "{} meinte: {}".format(user.nick, ret.strip()))

            if result:
                store.set('replace.{}.{}'.format(target, user.nick), result)
    else:
        store.set('replace.{}.{}'.format(target, user.nick), text)
