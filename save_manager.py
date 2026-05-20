import json
import os

SAVE_FILES = ["save_1.json", "save_2.json", "save_3.json"]
DEFAULT_DATA = {"playtime": 0.0, "deaths": 0, "deepest_floor": 0, "victories": 0}

def load_save(slot_index):
    path = SAVE_FILES[slot_index]
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            # На случай, если старое сохранение не имеет поля victories
            if "victories" not in data:
                data["victories"] = 0
            return data
    return DEFAULT_DATA.copy()

def save_data(slot_index, data):
    with open(SAVE_FILES[slot_index], 'w') as f:
        json.dump(data, f, indent=4)

def clear_save(slot_index):
    save_data(slot_index, DEFAULT_DATA.copy())
