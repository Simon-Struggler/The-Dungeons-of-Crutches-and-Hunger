import json
import os

SAVE_FILES = ["save_1.json", "save_2.json", "save_3.json"]
DEFAULT_DATA = {"playtime": 0.0, "deaths": 0, "deepest_floor": 0}

def load_save(slot_index):
    """Загружает данные сохранения (0, 1 или 2)."""
    path = SAVE_FILES[slot_index]
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(slot_index, data):
    """Сохраняет данные в файл."""
    with open(SAVE_FILES[slot_index], 'w') as f:
        json.dump(data, f, indent=4)

def clear_save(slot_index):
    """Очищает файл сохранения."""
    save_data(slot_index, DEFAULT_DATA.copy())