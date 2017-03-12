from bot import Bot
from registry import bot_command, REGISTRY


@bot_command('help')
def help(parsed, user, target, text):
    bot = Bot()

    bot.say(target, 'Hi, I\'m shackie. I\'ll react to the following commands: {}'.format(
        ', '.join(sorted(REGISTRY.keys()))
    ))
