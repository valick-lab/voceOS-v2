import os
import string
from core.state import state

def run(text: str):
    normalized = text.lower()
    if 'найди файл' in normalized:
        state["waiting_for"] = "search_file"
        return "Какой файл найти?"

    if 'покажи найденные файлы' in normalized or 'покажи файлы' in normalized or 'показать найденные' in normalized:
        if not state["found_files"]:
            return "Результатов поиска пока нет."
        result_lines = [f"Найденные файлы по запросу '{state['search_query']}':"]
        for i, file_path in enumerate(state["found_files"], 1):
            result_lines.append(f"{i}. {file_path}")
        return "\n".join(result_lines)
    
def handle_search(text: str):
    search_query = text.strip()
    drives = []
    for letter in string.ascii_uppercase:
        drive = letter + ":\\"
        if os.path.exists(drive):
            drives.append(drive)
    
    found_files = []
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if search_query.lower() in file.lower():
                    found_files.append(os.path.join(root, file))

    state["search_query"] = search_query
    state["found_files"] = found_files

    if not found_files:
        return "Файл не найден"
    if len(found_files) == 1:
        return f"Файл найден: {found_files[0]}"

    result_lines = [f"Найдено файлов: {len(found_files)}"]
    for i, file_path in enumerate(found_files, 1):
        result_lines.append(f"{i}. {file_path}")
    return "\n".join(result_lines)
