import glob
import importlib

import asyncio

import config
from bot import Bot
from registry import REGISTRY

if __name__ == '__main__':
    bot = Bot()

    print("### bot started")

    @bot.on('message')
    def bot_message(parsed, user, target, text):
        message = text
        if message.startswith(config.NICKNAME + ': '):
            message = message[len(config.NICKNAME) + 2:]

        if message.startswith(config.BOT_CHAR):
            command = message.split()[0]
            if len(command) > 1:
                command = command[1:]
                if command in REGISTRY:
                    REGISTRY[command](parsed, user, target, text)
                elif config.SAY_NO:
                    bot.say(target, 'I don\'t know what {} means.'.format(command))

    if config.PLUGINS == '__all__':
        module = glob.glob('plugins/*.py')
        module.sort()
        for m in module:
            importlib.import_module(m[:-3].replace('/', '.'))
    else:
        for plugin in config.PLUGINS:
            importlib.import_module('plugins.{}'.format(plugin))

    asyncio.get_event_loop().run_forever()
