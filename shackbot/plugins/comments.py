import random

import config
from bot import Bot
from .comment_data import ANSWERS, PERSONAL_ANSWERS

bot = Bot()


def _send_answer(answer, target):
    answer = random.choice(answer['answers'])
    if answer.startswith('/me'):
        answer = answer[4:]
        bot.writeln('PRIVMSG {target} :\x01ACTION {answer}\x01'.format(target=target, answer=answer))
    else:
        bot.say(target, answer)


@bot.on('message')
def comment(parsed, user, target, text):
    message = text
    addressed = False
    if message.startswith(config.NICKNAME + ': ') or message.startswith(config.NICKNAME + ', '):
        message = message[len(config.NICKNAME) + 2:]
        addressed = True

    if addressed:
        for answer in PERSONAL_ANSWERS:
            if answer['regex'].fullmatch(message):
                if random.random() <= answer['probability']:
                    _send_answer(answer, target)
                    return

    for answer in ANSWERS:
        if answer['regex'].fullmatch(message):
            if random.random() <= answer['probability']:
                _send_answer(answer, target)
                return
