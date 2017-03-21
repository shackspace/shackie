def get_command_if_bot_message(message, nickname, bot_char):
    """
    Strips leading nickname + ":|," if any, then returns a command if
    it is present.
    """
    if message.startswith(nickname + ': ') or message.startswith(nickname + ', '):
        message = message[len(nickname) + len(': ')]
        command = message.split()[0]
    elif message.startswith(bot_char):
        message = message[1:]
    else:
        return None
    command = message.split()[0]
    if len(command) > 1:
        command = command[1:]
