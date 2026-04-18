from commands import hello, off

commands_list = [
    hello, 
    off
    ]

def handle(text: str):
    for command in commands_list:
        result = command.run(text)
        if result:
            return result
    return None
