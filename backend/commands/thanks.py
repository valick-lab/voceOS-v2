from core.state import state

def run(text: str):
    text.lower()
    if 'спасибо' in text:
        return 'Всегда рад помочь!'