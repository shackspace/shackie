from bot import Bot
from registry import bot_command
from storage import store


bot = Bot()


@bot_command('karma')
def karma(parsed, user, target, text):
    text = text[len('.karma'):].strip()

    if not text:
        # print top/bottom
        pass

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

    response = ', '.join('{}: {}'.format(word, get_karma(target, word)) for word in to_print)
    bot.say(target, response)


@bot.on('message')
def title(parsed, user, target, text):
    text = text.strip()
    if text.endswith('++') or text.endswith('--'):
        karma = text[:-2]
        karma = karma.strip()
        if karma[0] in '"\'' and karma[0] == karma[-1]:
            karma = karma[1:-1]
        elif karma[0] == '(' and karma[-1] == ')':
            karma = karma[1:-1]

        if karma == user.nick:
            pass

        if text[-1] == '+':
            increment_karma(target, karma)
        else:
            decrement_karma(target, karma)


def get_karma(target, karma):
    return int(store.get('{}§{}'.format(target, karma)) or 0)


def increment_karma(target, karma):
    current = get_karma(target, karma)
    if not current:
        store.set('karma.{}§{}'.format(target, karma), 1)
    else:
        store.incr('karma.{}§{}'.format(target, karma), 1)
    update_scores(target, karma, current + 1)
    return current + 1


def decrement_karma(target, karma):
    current = get_karma(target, karma)
    if not current:
        store.set('karma.{}§{}'.format(target, karma), -1)
    else:
        store.decr('karma.{}§{}'.format(target, karma), 1)
    update_scores(target, karma, current - 1)
    return current - 1
