import curses
import time
from save_manager import load_save, clear_save

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def draw_centered(self, y, text, is_highlighted=False):
        height, width = self.stdscr.getmaxyx()
        x = max(0, (width - len(text)) // 2)
        try:
            if is_highlighted: self.stdscr.addstr(y, x, text, curses.A_REVERSE)
            else: self.stdscr.addstr(y, x, text)
        except curses.error: pass

    # --- ГЛАВНОЕ МЕНЮ И ФАЙЛЫ СОХРАНЕНИЯ ---
    def main_menu(self, keybindings):
        selected = 0
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (width - len("DUNGEONS OF CRUTCHES AND HUNGER")) // 2, "DUNGEONS OF CRUTCHES AND HUNGER")
            self.stdscr.addstr(4, (width - len("Select Save File:")) // 2, "Select Save File:")
            for i in range(3):
                data = load_save(i)
                text = f"Save {i+1} - Floor: {data['deepest_floor']} | Deaths: {data['deaths']}"
                display_text = f">> {text} <<" if i == selected else f"   {text}   "
                self.draw_centered(6 + i * 2, display_text, is_highlighted=(i == selected))
            self.stdscr.addstr(height - 2, (width - len("W/S: Navigate | ENTER: Select | ESC/Q: Quit")) // 2, "W/S: Navigate | ENTER: Select | ESC/Q: Quit")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected > 0: selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < 2: selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                action = self.save_info_menu(selected, keybindings)
                if action and action.get("start"): return action
            elif key in (27, ord('q')): exit()

    def save_info_menu(self, slot_index, keybindings):
        selected_option = 0
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            data = load_save(slot_index)
            self.stdscr.addstr(2, (width - len(f"Save File {slot_index + 1}")) // 2, f"Save File {slot_index + 1}")
            info_lines = [
                f"Playtime: {format_time(data['playtime'])}",
                f"Deaths: {data['deaths']}",
                f"Deepest Floor: {data['deepest_floor']}",
                f"Story Victories: {data.get('victories', 0)}" # Добавлено
            ]
            for i, line in enumerate(info_lines): self.draw_centered(4 + i, line)
            options = ["Select Save", "Clear Save"]
            for i, opt in enumerate(options):
                display_text = f">> {opt} <<" if i == selected_option else f"   {opt}   "
                self.draw_centered(9 + i * 2, display_text, is_highlighted=(i == selected_option))
            self.stdscr.addstr(height - 2, (width - len("ENTER: Confirm | ESC/Q: Back")) // 2, "ENTER: Confirm | ESC/Q: Back")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected_option > 0: selected_option -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected_option < 1: selected_option += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                if selected_option == 0: return self.game_mode_menu(slot_index, keybindings)
                elif selected_option == 1: clear_save(slot_index)
            elif key in (27, ord('q')): return None

    def game_mode_menu(self, slot_index, keybindings):
        options = [
            {"label": "Story mode", "enabled": True, "action": "story"},
            {"label": "Endless mode", "enabled": True, "action": "endless"},
            {"label": "Settings", "enabled": True, "action": "settings"},
            {"label": "Compendium", "enabled": False, "action": "compendium"},
            {"label": "Quit", "enabled": True, "action": "quit"}
        ]
        selected = next((i for i, opt in enumerate(options) if opt["enabled"]), 0)
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (width - len("Select Game Mode")) // 2, "Select Game Mode")
            for i, opt in enumerate(options):
                if i == selected and opt["enabled"]:
                    self.draw_centered(5 + i, f">> {opt['label']} <<", is_highlighted=True)
                else:
                    self.draw_centered(5 + i, f"   {opt['label']}   ")
            self.stdscr.addstr(height - 2, (width - len("W/S: Navigate | ENTER: Select | ESC/Q: Quit")) // 2, "W/S: Navigate | ENTER: Select | ESC/Q: Quit")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')):
                curr = selected
                while True:
                    curr = (curr - 1) % len(options)
                    if options[curr]["enabled"]: selected = curr; break
            elif key in (curses.KEY_DOWN, ord('s')):
                curr = selected
                while True:
                    curr = (curr + 1) % len(options)
                    if options[curr]["enabled"]: selected = curr; break
            elif key in (curses.KEY_ENTER, 10, 13):
                act = options[selected]["action"]
                if act == "story":
                    self.story_intro_menu() # Показываем лор
                    return self.endless_settings_menu(slot_index, keybindings, mode='story')
                elif act == "endless":
                    return self.endless_settings_menu(slot_index, keybindings, mode='endless')
                elif act == "settings": self.settings_menu(keybindings) # Передаем keybindings
                elif act == "quit": exit()
            elif key in (27, ord('q')): exit()

    # --- МЕНЮ НАСТРОЕК ---
    def settings_menu(self, keybindings):
        options = ['move_nw', 'move_ne', 'move_sw', 'move_se']
        display_names = {
            'move_nw': 'Move North-West', 'move_ne': 'Move North-East',
            'move_sw': 'Move South-West', 'move_se': 'Move South-East'
        }
        selected = 0
        
        # Зарезервированные клавиши, которые нельзя переназначить
        reserved = [ord('w'), ord('a'), ord('s'), ord('d'), ord('g'), ord('o'), ord('i'), ord('f'), ord('q'), ord('v'), ord('p'),
                    curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]

        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (width - len("SETTINGS")) // 2, "SETTINGS")
            
            for i, opt in enumerate(options):
                key_code = keybindings[opt]
                if key_code is None:
                    key_name = "Not Bound"
                elif key_code == curses.KEY_UP: key_name = "Up Arrow"
                elif key_code == curses.KEY_DOWN: key_name = "Down Arrow"
                elif key_code == curses.KEY_LEFT: key_name = "Left Arrow"
                elif key_code == curses.KEY_RIGHT: key_name = "Right Arrow"
                else:
                    try: key_name = chr(key_code).upper()
                    except ValueError: key_name = f"Key({key_code})"
                
                line = f"{display_names[opt]}: {key_name}"
                prefix = "> " if i == selected else "  "
                self.stdscr.addstr(5 + i * 2, (width - len(line) - 4) // 2, f"{prefix}{line}", 
                                   curses.A_REVERSE if i == selected else curses.A_NORMAL)

            self.stdscr.addstr(height-2, (width - len("ENTER: Rebind | ESC/Q: Back")) // 2, "ENTER: Rebind | ESC/Q: Back")
            self.stdscr.refresh()
            key = self.stdscr.getch()

            if key in (curses.KEY_UP, ord('w')) and selected > 0: selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < len(options)-1: selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                # Процесс перепривязки
                self.stdscr.addstr(height-4, (width - len("Press a new key to bind...")) // 2, "Press a new key to bind... (ESC to cancel)")
                self.stdscr.refresh()
                new_key = self.stdscr.getch()
                
                if new_key != 27: # Если не ESC
                    all_bound = [v for v in keybindings.values() if v is not None]
                    if new_key in reserved or new_key in all_bound:
                        self.stdscr.addstr(height-4, (width - len("That key is already in use!")) // 2, "That key is already in use!     ")
                        self.stdscr.refresh()
                        self.stdscr.getch()
                    else:
                        keybindings[options[selected]] = new_key
            elif key in (27, ord('q')):
                break
            
    # --- ПРЕДИСТОРИЯ СЮЖЕТНОГО РЕЖИМА ---
    def story_intro_menu(self):
        lore_text = [
            "DUNGEONS OF CRUTCHES AND HUNGER",
            "",
            "The kingdom fell not to war, but to the Great Famine.",
            "Desperate for salvation, the mad King delved into the ancient",
            "depths beneath the castle, seeking a cursed artifact rumored to",
            "grant eternal life. He never returned.",
            "",
            "Now, a creeping mist rises from the dungeons, turning the",
            "starving into ravenous beasts and the dead into tireless sentinels.",
            "As a desperate wanderer, you descend into the abyss, seeking",
            "either the King's salvation or an end to your own suffering.",
            "",
            "Legends speak of a porcelain White Mask on the lowest level,",
            "an artifact that holds dominion over the dungeon's nightmares.",
            "Find it, and perhaps you will finally find peace...",
            "or become the nightmare yourself."
        ]
        
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            
            start_y = max(2, (height - len(lore_text)) // 2)
            for i, line in enumerate(lore_text):
                x = (width - len(line)) // 2
                try: self.stdscr.addstr(start_y + i, x, line)
                except: pass
                
            self.stdscr.addstr(height - 2, (width - len("Press ENTER to begin your descent...")) // 2, "Press ENTER to begin your descent...")
            self.stdscr.refresh()
            
            key = self.stdscr.getch()
            if key in (curses.KEY_ENTER, 10, 13):
                break

    def endless_settings_menu(self, slot_index, keybindings, mode='endless'):
        sizes = [
            {"label": "Small (60x20)", "w": 60, "h": 20},
            {"label": "Medium (80x24)", "w": 80, "h": 24},
            {"label": "Large (100x28)", "w": 100, "h": 28},
            {"label": "Extra Large (120x32)", "w": 120, "h": 32}
        ]
        selected_size = 2
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (width - len("Select Map Size")) // 2, "Select Map Size")
            for i, sz in enumerate(sizes):
                display_text = f">> {sz['label']} <<" if i == selected_size else f"   {sz['label']}   "
                self.draw_centered(5 + i, display_text, is_highlighted=(i == selected_size))
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected_size > 0: selected_size -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected_size < len(sizes)-1: selected_size += 1
            elif key in (curses.KEY_ENTER, 10, 13): break

        diffs = ["Easy", "Medium", "Difficult"]
        selected_diff = 1
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (width - len("Select Difficulty")) // 2, "Select Difficulty")
            for i, df in enumerate(diffs):
                display_text = f">> {df} <<" if i == selected_diff else f"   {df}   "
                self.draw_centered(5 + i, display_text, is_highlighted=(i == selected_diff))
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected_diff > 0: selected_diff -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected_diff < len(diffs)-1: selected_diff += 1
            elif key in (curses.KEY_ENTER, 10, 13): break

        return {"start": True, "slot": slot_index, "mode": mode, "width": sizes[selected_size]["w"], "height": sizes[selected_size]["h"], "difficulty": diffs[selected_diff].lower()}

    # --- МЕНЮ ЛУТА (ПОДБОР С ПОЛА) ---
    def loot_menu(self, items_on_floor):
        selected = 0
        selected_indices = set() # Множество для галочек (выбрано/не выбрано)
        
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(1, 2, "ITEMS ON FLOOR (Select and press 'g' to grab)")
            
            for i, item in enumerate(items_on_floor):
                check = "[X]" if i in selected_indices else "[ ]"
                line = f"{check} {item.name} x{item.quantity}"
                self.stdscr.addstr(3 + i, 2, line, curses.A_REVERSE if i == selected else curses.A_NORMAL)
                
            self.stdscr.addstr(height-2, 2, "W/S: Navigate | ENTER: Toggle | G: Grab selected | ESC/Q: Close")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            
            if key in (curses.KEY_UP, ord('w')) and selected > 0: selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < len(items_on_floor)-1: selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                # Переключаем галочку
                if selected in selected_indices: selected_indices.remove(selected)
                else: selected_indices.add(selected)
            elif key == ord('g'):
                if selected_indices:
                    return list(selected_indices) # Возвращаем индексы выбранных предметов
                else:
                    # Если не выбрали ни одного, берем тот, на котором стоит курсор
                    return [selected]
            elif key in (27, ord('q')): # ESC
                return []

        # --- ВНУТРИИГРОВОЕ МЕНЮ (3 КОЛОНКИ) ---
    def inventory_menu(self, player, engine):
        active_panel = 0 # 0 = Статы, 1 = Экипировка, 2 = Рюкзак
        selected_stat = 0
        selected_equip_slot = 0
        selected_item = 0

        stat_keys = ['str', 'dex', 'con']
        stat_names = ['Strength', 'Dexterity', 'Constitution']
        equip_slots = list(player.equipment.keys())

        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            
            col1_end = width // 3
            col2_end = 2 * (width // 3)
            
            for y in range(height): 
                self.stdscr.addch(y, col1_end, '|')
                self.stdscr.addch(y, col2_end, '|')

            # --- Колонка 1: Характеристики ---
            self.stdscr.addstr(1, 2, f"STATS (Pts: {player.stat_points})")
            for i, name in enumerate(stat_names):
                base_val = getattr(player, f"{stat_keys[i]}_stat")
                total_val = getattr(player, f"get_total_{stat_keys[i]}")()
                bonus = total_val - base_val
                cost = player.get_stat_cost(stat_keys[i])
                prefix = "> " if active_panel == 0 and selected_stat == i else "  "
                
                stat_str = f"{base_val}(+{bonus})" if bonus > 0 else str(base_val)
                line = f"{prefix}{name[:3]}: {stat_str} (Cost:{cost})"
                self.stdscr.addstr(3 + i*2, 2, line, curses.A_REVERSE if active_panel == 0 and selected_stat == i else curses.A_NORMAL)

            # --- Колонка 2: Экипировка ---
            self.stdscr.addstr(1, col1_end + 2, "EQUIPMENT")
            for i, slot in enumerate(equip_slots):
                item = player.equipment[slot]
                prefix = "> " if active_panel == 1 and selected_equip_slot == i else "  "
                slot_name = slot.replace('_', ' ').title()
                item_name = item.name if item else "[Empty]"
                line = f"{prefix}{slot_name[:5]}: {item_name}"
                self.stdscr.addstr(3 + i, col1_end + 2, line, curses.A_REVERSE if active_panel == 1 and selected_equip_slot == i else curses.A_NORMAL)

            # --- Колонка 3: Рюкзак ---
            self.stdscr.addstr(1, col2_end + 2, "BACKPACK")
            inv = player.inventory
            if not inv:
                self.stdscr.addstr(3, col2_end + 2, "Empty")
            else:
                for i, item in enumerate(inv):
                    prefix = "> " if active_panel == 2 and selected_item == i else "  "
                    line = f"{prefix}{item.name} x{item.quantity}"
                    self.stdscr.addstr(3 + i, col2_end + 2, line, curses.A_REVERSE if active_panel == 2 and selected_item == i else curses.A_NORMAL)

            self.stdscr.addstr(height-2, 2, "A/D: Switch Panel | W/S: Navigate | ENTER: Action | ESC/I/Q: Close")
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key in (curses.KEY_UP, ord('w')):
                if active_panel == 0 and selected_stat > 0: selected_stat -= 1
                elif active_panel == 1 and selected_equip_slot > 0: selected_equip_slot -= 1
                elif active_panel == 2 and selected_item > 0: selected_item -= 1
            elif key in (curses.KEY_DOWN, ord('s')):
                if active_panel == 0 and selected_stat < 2: selected_stat += 1
                elif active_panel == 1 and selected_equip_slot < len(equip_slots)-1: selected_equip_slot += 1
                elif active_panel == 2 and inv and selected_item < len(inv)-1: selected_item += 1
            elif key in (curses.KEY_LEFT, ord('a')):
                if active_panel > 0: active_panel -= 1
            elif key in (curses.KEY_RIGHT, ord('d')):
                if active_panel == 0: active_panel = 1
                elif active_panel == 1 and inv: active_panel = 2
            elif key in (curses.KEY_ENTER, 10, 13):
                if active_panel == 0:
                    stat_name = stat_keys[selected_stat]
                    # Вызываем новое контекстное меню для статов
                    self.stat_context_menu(player, stat_name)
                elif active_panel == 1:
                    slot_name = equip_slots[selected_equip_slot]
                    if player.equipment[slot_name]:
                        ctx_result = self.equipment_context_menu(player, slot_name, engine)
                elif active_panel == 2 and inv:
                    item = inv[selected_item]
                    ctx_result = self.item_context_menu(player, item, engine)
                    if ctx_result:
                        if selected_item >= len(player.inventory) and selected_item > 0:
                            selected_item = len(player.inventory) - 1
            elif key in (ord('i'), ord('q'), 27):
                break

        # --- КОНТЕКСТНОЕ МЕНЮ ХАРАКТЕРИСТИК ---
    def stat_context_menu(self, player, stat_name):
        options = ["Upgrade", "Info"]
        selected = 0
        pending_confirm = False

        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            
            val = getattr(player, f"{stat_name}_stat")
            cost = player.get_stat_cost(stat_name)
            nice_name = stat_name.upper()
            
            self.stdscr.addstr(1, 2, f"{nice_name}: {val} (Upgrade Cost: {cost})")
            
            for i, opt in enumerate(options):
                prefix = "> " if i == selected else "  "
                if i == 0 and pending_confirm:
                    opt_text = f"{opt} [CONFIRM?]"
                else:
                    opt_text = opt
                self.stdscr.addstr(3 + i, 2, f"{prefix}{opt_text}", curses.A_REVERSE if i == selected else curses.A_NORMAL)
                
            self.stdscr.addstr(height-2, 2, "W/S: Navigate | ENTER: Select | ESC/Q: Back")
            self.stdscr.refresh()
            
            key = self.stdscr.getch()
            
            if key in (curses.KEY_UP, ord('w')) and selected > 0:
                pending_confirm = False
                selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < len(options)-1:
                pending_confirm = False
                selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                if selected == 0: # Upgrade
                    if pending_confirm:
                        if player.increase_stat(stat_name):
                            pending_confirm = False
                            break # Успешно прокачали, закрываем меню
                        else:
                            pending_confirm = False # Не хватило очков, сбрасываем
                    else:
                        pending_confirm = True
                elif selected == 1: # Info
                    self.stdscr.clear()
                    desc = player.get_stat_description(stat_name)
                    self.stdscr.addstr(1, 2, desc)
                    self.stdscr.addstr(3, 2, "Press any key to close...")
                    self.stdscr.refresh()
                    self.stdscr.getch()
            elif key in (27, ord('q')):
                break

    # --- НОВОЕ: КОНТЕКСТНОЕ МЕНЮ НАДЕТОЙ ЭКИПИРОВКИ ---
    def equipment_context_menu(self, player, slot_name, engine):
        options = ["Unequip", "Info"]
        selected = 0
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            item = player.equipment[slot_name]
            self.stdscr.addstr(1, 2, f"Equipped: {item.name}")
            for i, opt in enumerate(options):
                self.stdscr.addstr(3 + i, 2, opt, curses.A_REVERSE if i == selected else curses.A_NORMAL)
            self.stdscr.addstr(height-2, 2, "W/S: Navigate | ENTER: Select | ESC/Q: Back")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected > 0: selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < len(options)-1: selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                choice = options[selected]
                if choice == "Unequip":
                    msg = player.unequip_item(slot_name)
                    engine.message = msg
                    return True
                elif choice == "Info":
                    self.stdscr.clear()
                    self.stdscr.addstr(1, 2, item.description)
                    self.stdscr.addstr(3, 2, "Press any key to close...")
                    self.stdscr.refresh()
                    self.stdscr.getch()
            elif key in (27, ord('q')): return False

    # --- ОБНОВЛЕННОЕ КОНТЕКСТНОЕ МЕНЮ РЮКЗАКА ---
    def item_context_menu(self, player, item, engine):
        options = []
        if item.category == 'consumable':
            options.append("Use")
        elif item.category == 'equipment':
            options.append("Equip")
        
        options.append("Info")
        
        if item.category != 'key':
            options.append("Drop 1")

        selected = 0
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            self.stdscr.addstr(1, 2, f"{item.name} x{item.quantity}")
            for i, opt in enumerate(options):
                self.stdscr.addstr(3 + i, 2, opt, curses.A_REVERSE if i == selected else curses.A_NORMAL)
            self.stdscr.addstr(height-2, 2, "W/S: Navigate | ENTER: Select | ESC/Q: Back")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')) and selected > 0: selected -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and selected < len(options)-1: selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                choice = options[selected]
                if choice == "Use":
                    msg = player.use_item(item)
                    engine.message = msg
                    return True
                elif choice == "Equip":
                    msg = player.equip_item(item)
                    engine.message = msg
                    return True
                elif choice == "Info":
                    self.stdscr.clear()
                    self.stdscr.addstr(1, 2, item.description)
                    self.stdscr.addstr(3, 2, "Press any key to close...")
                    self.stdscr.refresh()
                    self.stdscr.getch()
                elif choice == "Drop 1":
                    engine.drop_item(item, 1)
                    return True
            elif key in (27, ord('q')): return False
