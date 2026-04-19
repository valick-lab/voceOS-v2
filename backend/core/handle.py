from core.state import state
from commands import off, hello, search_file

commands_list = [
    off,
    hello,
    search_file
]

def handle(text: str):
    text = text.lower()

    if state["waiting_for"] == "off_time":
        text.lower()
        return off.handle_time(text)
    
    elif state["waiting_for"] == "search_file":
        state["waiting_for"] = None
        return search_file.handle_search(text)

    for cmd in commands_list:
        result = cmd.run(text)
        if result:
            return result

    return None