import os
import string
from core.state import state

def run (text:str):
    normalized = text.lower()
    if "открой файл" in normalized:
        state["waiting_for"] = "open_file"
        return 'назовите файл, который хотите открыть:'

def handle_open(text:str):
    open_query = text.strip()
    drives = []
    for letter in string.ascii_uprase:
        
    