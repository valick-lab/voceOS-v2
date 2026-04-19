import os
import string
from core.state import state

def run(text: str):
    if 'найди файл' in text.lower():
        state["waiting_for"] = "search_file"
        return "Какой файл найти?"
    
def handle_search(text: str):
    drives = []
    for letter in string.ascii_uppercase:
        drive = letter + ":\\"
        if os.path.exists(drive):
            drives.append(drive)
    
    found_files = []
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if text.lower() in file.lower():
                    found_files.append(os.path.join(root, file))

    if not found_files:
        return "Файл не найден"
    if len(found_files) == 1:
        return f"Файл найден: {found_files[0]}"

    result_lines = [f"Найдено файлов: {len(found_files)}"]
    result_lines.extend(found_files)
    return "\n".join(result_lines)
