from bot import Bot
from registry import bot_command, REGISTRY


@bot_command('help')
def help(parsed, user, target, text):
    bot = Bot()

    bot.say('Hi, I\'m shackie. I\'ll react to the following commands: {}'.format(
        ', '.join(REGISTRY.keys())
    ))
