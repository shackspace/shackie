from bot import Bot
from main import bot_command
from storage import store


@bot_command('status')
def status(parsed, user, target, text):
    bot = Bot()
    _status = store.get('status')
    if not _status:
        _status = 0
    else:
        _status = int(_status)
    print(type(_status))
    store.incr('status', 1)
    bot.say(target, "everything is ok, {} [{}]".format(user.nick, _status))
