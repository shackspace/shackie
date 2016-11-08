"""
via http://cgit.cd.krebsco.de/stockholm/tree/krebs/5pkgs/Reaktor/scripts/sed-plugin.py
"""
import re
from subprocess import Popen, PIPE
from shutil import which
from os.path import realpath

from bot import Bot
from storage import store


bot = Bot()


def is_replace(line):
    myre = re.compile(r'^s/((?:\\/|[^/])+)/((?:\\/|[^/])*)/([ig]*)$')
    return myre.match(line)


@bot.on('message')
def replace_entrypoint(parsed, user, target, text):
    regex = is_replace(text)
    if regex:
        last_line = store.get('replace.{}.{}'.format(target, user.nick)).decode()
        if last_line:
            source, destination, flagstr = regex.groups()
            source = source.replace('\/','/')
            destination = destination.replace('\/','/')
            flagstr = flagstr or ''

            # do not trust sed as it is able to read and write arbitrary files
            p = Popen(['proot',
                            '-b','/usr',
                            '-b','/bin',
                            # TODO: additional folders may be required
                            '-r','/var/empty',
                            '-w','/',
                            realpath(which('sed')),
                            's/{}/{}/{}'.format(source,destination,flagstr)
                        ], stdin=PIPE, stdout=PIPE )

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
