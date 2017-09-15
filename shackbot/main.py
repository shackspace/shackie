#!/usr/bin/env python3

import glob
import importlib
from inspect import iscoroutinefunction

import asyncio

import config
from bot import Bot
from core.parsing import get_command_if_bot_message
from registry import REGISTRY


if __name__ == '__main__':
    bot = Bot()

    print("### bot started")

    @bot.on('message')
    def bot_message(parsed, user, target, text):
        command = get_command_if_bot_message(text, config.NICKNAME, config.BOT_CHAR)
        if command:
            if command in REGISTRY:
                try:
                    handler = REGISTRY[command]
                    if (iscoroutinefunction(handler)):
                        asyncio.ensure_future(handler(parsed, user, target, text))
                    else:
                        handler(parsed, user, target, text)
                except Exception as e:
                    print('Calling "{command} failed. Exception: {e}"'.format(command=command, e=str(e)))
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
