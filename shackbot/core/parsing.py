def get_command_if_bot_message(message, nickname, bot_char):
    """
    Strips leading nickname + ":|," if any, then returns a command if
    it is present.
    """
    if message.startswith(nickname + ': ') or message.startswith(nickname + ', '):
        message = message[len(nickname) + len(': ')]
        command = message.split()[0]
        if command.startswith(bot_char):
            return command[1:]
        return command

    elif message.startswith(bot_char):
        message = message[1:]
        return message.split()[0]
