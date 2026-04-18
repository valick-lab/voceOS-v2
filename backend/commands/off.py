import os
from core.state import state
import re

def run(text: str):
    if "выключи компьютер" in text.lower():

        if "через" in text.lower():
            state["waiting_for"] = "off_time"
            text.lower()
            return "Через сколько времени выключить компьютер?"

        else:
            os.system("shutdown /s /t 10")
            return "Выключаю компьютер через 10 секунд"


def handle_time(text: str):
    state["waiting_for"] = None
    text.lower()
    match = re.search(r"\d+", text)

    if match:
        seconds = int(match.group()) * 60
        os.system(f"shutdown /s /t {seconds}")
        return f"Выключаю компьютер через {seconds} секунд"

    return "Не понял время"