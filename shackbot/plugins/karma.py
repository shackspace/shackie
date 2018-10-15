import json
import operator

from bot import Bot
from config import IGNORE
from registry import bot_command
from storage import store


bot = Bot()


@bot_command('karma')
def show_karma(parsed, user, target, text):
    if user.nick in IGNORE:
        return

    text = text[len('.karma'):].strip().lower()
    if not text:
        try:
            top = json.loads(store.get('karma.top.{}'.format(target)).decode()) or dict()
            bottom = json.loads(store.get('karma.bottom.{}'.format(target)).decode()) or dict()
        except AttributeError:
            store.set('karma.top.{}'.format(target), dict())
            store.set('karma.bottom.{}'.format(target), dict())
        else:
            user_karma = get_karma(target, user.nick)

            response = 'Top karma: {}. Flop karma: {}. Karma for {}: {}'.format(
                ', '.join('{}: {}'.format(key, value) for key, value in top.items()),
                ', '.join('{}: {}'.format(key, value) for key, value in bottom.items()),
                user.nick, user_karma,
            )
            bot.say(target, response)

    else:
        to_print = []
        in_literal = []
        for word in text.split():
            if in_literal:
                if word.endswith('"'):
                    in_literal.append(word[:-1])
                    to_print.append(' '.join(in_literal))
                    in_literal = []
                else:
                    in_literal.append(word)

            elif word.startswith('"'):
                if word.endswith('"'):
                    to_print.append(word[1:-1])
                else:
                    in_literal.append(word[1:])

            else:
                to_print.append(word)

        response = ', '.join('{}: {}'.format(word, get_karma(target, word.lower())) for word in to_print)
        bot.say(target, response)


@bot.on('message')
def title(parsed, user, target, text):
    if user.nick in IGNORE:
        return
    text = text.strip()
    if text.endswith('++') or text.endswith('--'):
        karma = text[:-2]
        karma = karma.strip().lower()
        if karma[0] in '"\'' and karma[0] == karma[-1]:
            karma = karma[1:-1]
        elif karma[0] == '(' and karma[-1] == ')':
            karma = karma[1:-1]

        if karma == user.nick.lower():
            pass

        if text[-1] == '+':
            increment_karma(target, karma)
        else:
            decrement_karma(target, karma)


def get_karma(target, karma):
    return int(store.get('karma.{}§{}'.format(target, karma.lower())) or 0)


def update_scores(target, karma, value):
    try:
        top = json.loads(store.get('karma.top.{}'.format(target)).decode()) or dict()
        bottom = json.loads(store.get('karma.bottom.{}'.format(target)).decode()) or dict()
    except:
        top = dict()
        bottom = dict()

    top.update({karma: value})
    bottom.update({karma: value})
    top = dict(sorted(top.items(), key=operator.itemgetter(1), reverse=True)[:3])
    bottom = dict(sorted(bottom.items(), key=operator.itemgetter(1), reverse=False)[:3])
    store.set('karma.top.{}'.format(target), json.dumps(top))
    store.set('karma.bottom.{}'.format(target), json.dumps(bottom))


def increment_karma(target, karma):
    target = target.lower()
    current = get_karma(target, karma)
    if not current:
        store.set('karma.{}§{}'.format(target, karma), 1)
    else:
        store.incr('karma.{}§{}'.format(target, karma), 1)
    update_scores(target, karma, current + 1)
    return current + 1


def decrement_karma(target, karma):
    target = target.lower()
    current = get_karma(target, karma)
    if not current:
        store.set('karma.{}§{}'.format(target, karma), -1)
    else:
        store.decr('karma.{}§{}'.format(target, karma), 1)
    update_scores(target, karma, current - 1)
    return current - 1
