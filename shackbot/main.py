import asyncio
import glob
import importlib

import config
from bot import Bot
from storage import store
from registry import bot_command, REGISTRY


if __name__ == '__main__':
    bot = Bot()

    @bot.on('message')
    def bot_message(parsed, user, target, text):
        if text.startswith(config.BOT_CHAR):
            command = text.split()[0]
            if len(command) > 1:
                command = command[1:]
                if command in REGISTRY:
                    REGISTRY[command](parsed, user, target, text)
                elif config.SAY_NO:
                    bot.say(target, 'I don\'t know what {} means.'.format(command))

    module = glob.glob('plugins/*.py')
    module.sort()
    for m in module:
        importlib.import_module(m[:-3].replace('/', '.'))

    asyncio.get_event_loop().run_forever()
