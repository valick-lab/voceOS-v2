from core.state import state
import os
import string

def run(text: str):
    if 'открой файл' in text.lower():
        state["waiting_for"] = "open_file"
        return "Какой файл открыть?"
    
def handle_open(text: str):
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
        os.startfile(found_files[0])
        return f"Файл найден: {found_files[0]}"
    
    state["waiting_for"] = "select_file"
    result_lines = [f"Найдено файлов: {len(found_files)}\nКакой файл нужно открыть?(назовите номер)"]
    for i, file_path in enumerate(found_files, 1):
        result_lines.append(f"{i}. {file_path}")
    
    return "\n".join(result_lines)

def handle_select_file(text: str):
    try:
        file_number = int(text.strip())
        if 1 <= file_number <= len(state["found_files"]):
            selected_file = state["found_files"][file_number - 1]
            os.startfile(selected_file)
            state["waiting_for"] = None
            return f"Открывается: {selected_file}"
        else:
            return f"Пожалуйста, введите номер от 1 до {len(state['found_files'])}"
    except ValueError:
        return "Пожалуйста, назовите номер файла"
