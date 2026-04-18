from core.state import state
from commands import off, hello

commands_list = [
    off,
    hello
]

def handle(text: str):
    text = text.lower()

    if state["waiting_for"] == "off_time":
        text.lower()
        return off.handle_time(text)

    for cmd in commands_list:
        result = cmd.run(text)
        if result:
            return result

    return None