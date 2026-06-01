import json
import os
from core.compendium import ENEMY_TEMPLATES, ITEM_TEMPLATES

SAVE_FILES = ["save_1.json", "save_2.json", "save_3.json"]

def _generate_default_compendium():
    """Генерирует пустой компендиум на основе шаблонов."""
    compendium = {"enemies": {}, "items": {}}
    for name in ENEMY_TEMPLATES.keys():
        compendium["enemies"][name] = {"discovered": False, "kills": 0, "deaths_by": 0}
    for name in ITEM_TEMPLATES.keys():
        compendium["items"][name] = {"discovered": False}
    return compendium

DEFAULT_DATA = {"playtime": 0.0, "deaths": 0, "deepest_floor": 0, "victories": 0, "compendium": _generate_default_compendium()}

def load_save(slot_index):
    path = SAVE_FILES[slot_index]
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            # Поддержка старых сохранений и добавление новых записей
            if "victories" not in data: data["victories"] = 0
            if "compendium" not in data: 
                data["compendium"] = _generate_default_compendium()
            else:
                # Добавляем новых врагов/предметы, которых не было в старом сохранении
                default_comp = _generate_default_compendium()
                for cat in ["enemies", "items"]:
                    for name, val in default_comp[cat].items():
                        if name not in data["compendium"][cat]:
                            data["compendium"][cat][name] = val
            return data
    return DEFAULT_DATA.copy()

def save_data(slot_index, data):
    with open(SAVE_FILES[slot_index], 'w') as f:
        json.dump(data, f, indent=4)

def clear_save(slot_index):
    save_data(slot_index, DEFAULT_DATA.copy())