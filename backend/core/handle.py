from core.state import state
from commands import off, hello, search_file, open_file, thanks

commands_list = [
    off,
    hello,
    search_file,
    open_file,
    thanks
]

def handle(text: str):
    text = text.lower()

    if state["waiting_for"] == "off_time":
        text.lower()
        return off.handle_time(text)
    
    elif state["waiting_for"] == "search_file":
        state["waiting_for"] = None
        return search_file.handle_search(text)
    elif state["waiting_for"] == "open_file":
        return open_file.handle_open(text)
    elif state["waiting_for"] == "select_file":
        state["waiting_for"] = None
        return open_file.handle_select_file(text)

    for cmd in commands_list:
        result = cmd.run(text)
        if result:
            return result

    return None