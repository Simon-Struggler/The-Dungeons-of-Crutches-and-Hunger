import curses
import random
import time
from ui.renderer import Renderer
from actions.commands import MoveCommand, DescendCommand, WaitCommand, GetCommand, AttackCommand
from map_gen.dungeon import generate_dungeon
from actors.player import Player
from items.item import RatMeat, DungeonKey, Item, OldSword, HatOfKnowledge, Glasses, Chainmail, GlovesOfDexterity, Spear, Buckler, LeggingsOfStrength, AchillesSandals
from save_manager import load_save, save_data
from menu import Menu

class Engine:
    def __init__(self, stdscr, settings, keybindings):
        self.stdscr = stdscr
        self.renderer = Renderer(stdscr)
        self.current_floor = 1
        self.message = ""
        
        # Извлекаем настройки
        self.save_slot = settings["slot"]
        self.game_mode = settings["mode"]
        self.map_width = settings["width"]
        self.map_height = settings["height"]
        self.difficulty = settings["difficulty"]
        self.keybindings = keybindings

        self.save_data = load_save(self.save_slot)
        self.session_start_time = time.time()
        self.player_actions_taken = 0
        self.awaiting_open_direction = False

        self.battle_log = [] # Лог боя
        self.max_log_lines = 100
        self.spawned_equipment_names = set() # Память о том, какая экипировка уже выпадала
        self.chests = []
        self.turn_counter = 0 # Счетчик ходов для системы голода
        self.awaiting_quit_confirm = False # Состояние ожидания подтверждения выхода
        self.awaiting_attack_direction = False # Ожидание направления для атаки

        term_height, term_width = self.stdscr.getmaxyx()
        if term_height < self.map_height or term_width < self.map_width:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Terminal too small! Need {self.map_width}x{self.map_height}")
            self.stdscr.refresh()
            self.stdscr.getch()
            exit(1)

        self.game_map, player_x, player_y, self.enemies, self.items, self.chests = generate_dungeon(self.map_width, self.map_height, first_floor=True, current_floor=self.current_floor)
        self.player = Player(player_x, player_y)
        self.player.engine_ref = self
        
        # Раздаем ссылку на движок всем врагам при создании уровня
        for enemy in self.enemies:
            enemy.engine_ref = self

    def update_playtime_and_save(self):
        current_time = time.time()
        elapsed = current_time - self.session_start_time
        self.save_data['playtime'] += elapsed
        self.session_start_time = current_time
        save_data(self.save_slot, self.save_data)

    def go_downstairs(self):
        self.current_floor += 1
        if self.current_floor > self.save_data['deepest_floor']:
            self.save_data['deepest_floor'] = self.current_floor
            self.update_playtime_and_save()
            
        px, py = self.player.x, self.player.y
        self.game_map, _, _, self.enemies, self.items, self.chests = generate_dungeon(
            self.map_width, self.map_height, player_x=px, player_y=py, first_floor=False, current_floor=self.current_floor
        )
        self.player_actions_taken = 0
        
        # Раздаем ссылку на движок врагам на новом этаже
        for enemy in self.enemies:
            enemy.engine_ref = self

    def handle_enemy_deaths(self):
        dead_enemies = []
        for enemy in self.enemies:
            if not enemy.is_alive():
                dead_enemies.append(enemy)
                self.add_log(f"The {enemy.char} dies!")
                
                old_level = self.player.level
                self.player.gain_xp(enemy.xp_reward)
                if self.player.level > old_level:
                    self.add_log(f"LEVEL UP! You are now level {self.player.level}!")
                
                if enemy.char == 'G':
                    self.items.append(DungeonKey(enemy.x, enemy.y))
                elif enemy.char == 'r' and random.random() < 0.5:
                    self.items.append(RatMeat(enemy.x, enemy.y))
                elif enemy.char == 'S':
                    self.items.append(OldSword(enemy.x, enemy.y))
        for enemy in dead_enemies:
            self.enemies.remove(enemy)

    def generate_chest_loot(self):
        """Генерирует 2-4 предмета для сундука. Гарантирует уникальную экипировку внутри."""
        loot = []
        spawned_names_this_chest = set() # Следим за дубликатами в ЭТОМ сундуке
        available_equipment = [OldSword, HatOfKnowledge, Glasses, Chainmail, GlovesOfDexterity, Spear, Buckler, LeggingsOfStrength, AchillesSandals]
        
        # Фильтруем экипировку, которую ещё не видели за весь забег
        unseen_equipment = [eq for eq in available_equipment if eq.__name__ not in self.spawned_equipment_names]
        if not unseen_equipment:
            unseen_equipment = available_equipment
            
        # 1 гарантированный предмет экипировки
        eq_class = random.choice(unseen_equipment)
        loot.append(eq_class(0, 0))
        self.spawned_equipment_names.add(eq_class.__name__)
        spawned_names_this_chest.add(eq_class.__name__)
        
        # От 1 до 3 дополнительных предметов (consumables или equipment)
        for _ in range(random.randint(1, 3)):
            if random.random() < 0.6:
                loot.append(RatMeat(0, 0))
            else:
                # Исключаем то, что уже выпало в этом сундуке
                possible_eq = [eq for eq in available_equipment if eq.__name__ not in spawned_names_this_chest]
                
                if not possible_eq:
                    # Если нам совсем не повезло и вся экипировка уже в сундуке, даём мясо вместо дубликата
                    loot.append(RatMeat(0, 0))
                    continue
                    
                eq_class = random.choice(possible_eq)
                loot.append(eq_class(0, 0))
                self.spawned_equipment_names.add(eq_class.__name__)
                spawned_names_this_chest.add(eq_class.__name__)
                
        return loot
    
    def handle_get(self):
        """Обработка нажатия кнопки 'g' (подобрать предмет)."""
        items_here = [i for i in self.items if i.x == self.player.x and i.y == self.player.y]
        if not items_here:
            self.message = "Nothing to pick up here."
            return

        if len(items_here) == 1:
            item = items_here[0]
            if self.player.add_item(item):
                self.items.remove(item)
                self.message = f"Picked up {item.name}."
            else:
                self.message = f"You have enough '{item.name}' already."
        else:
            # Если предметов несколько, открываем меню лута
            picked_indices = Menu(self.stdscr).loot_menu(items_here)
            
            # Собираем выбранные предметы (перебираем в обратном порядке, чтобы индексы не сбились при удалении)
            for index in sorted(picked_indices, reverse=True):
                item = items_here[index]
                if self.player.add_item(item):
                    self.items.remove(item)
                    self.message = f"Picked up {item.name}."
                else:
                    self.message = f"Cannot pick up {item.name}."

    def drop_item(self, item, qty=1):
        """Выкидывает предмет из инвентаря на пол."""
        if item in self.player.inventory:
            # Создаем копию предмета для пола с текущими координатами игрока
            dropped_item = Item(item.x, item.y, item.name, item.char, item.category, item.description, item.max_stack, qty)
            dropped_item.x = self.player.x
            dropped_item.y = self.player.y
            
            self.items.append(dropped_item)
            self.player.remove_item(item, qty)
            self.message = f"Dropped {item.name} x{qty}."

    def wake_enemies_in_explored(self):
        """Пробуждает всех спящих врагов на исследованных клетках."""
        for enemy in self.enemies:
            if enemy.is_alive() and self.game_map.explored[enemy.y][enemy.x]:
                if hasattr(enemy.ai, 'is_awake'):
                    enemy.ai.is_awake = True

    def add_log(self, msg):
        """Добавляет сообщение в лог боя."""
        self.battle_log.append(msg)
        if len(self.battle_log) > self.max_log_lines:
            self.battle_log.pop(0)

    def resolve_attack(self, attacker, defender):
        """Обрабатывает атаку от attacker к defender, возвращает True если защитник выжил."""
        is_player_attacking = (attacker.char == '@')
        atk_name = "You" if is_player_attacking else f"The {attacker.char}"
        def_name = "you" if not is_player_attacking else f"the {defender.char}"
        
        damage = attacker.get_attack_damage()
        is_crit = random.randint(1, 100) <= attacker.get_crit_chance()
        
        if is_crit:
            damage *= 2 # Удваиваем сырое значение урона
            
            # Вызываем take_damage с флагом is_crit=True (важно для Buckler)
            actual_dmg = defender.take_damage(damage, is_crit=True)
            
            # Спец-сообщение для Щита: если урон не удвоился, значит щит поглотил крит
            if is_player_attacking and actual_dmg < damage and actual_dmg > 0:
                 self.add_log(f"CRITICAL! {atk_name} hit {def_name}, but they blocked part of it for {actual_dmg} damage!")
            else:
                 self.add_log(f"CRITICAL! {atk_name} hit {def_name} for {actual_dmg} damage!")
        else:
            if defender.try_dodge():
                if is_player_attacking:
                    self.add_log(f"{def_name.capitalize()} dodged your attack!")
                else:
                    self.add_log(f"You dodged {atk_name.lower()}'s attack!")
                return True
            else:
                actual_dmg = defender.take_damage(damage, is_crit=False)
                self.add_log(f"{atk_name} hit {def_name} for {actual_dmg} damage.")
        
        return defender.is_alive()

    def run(self):
        while True:
            self.renderer.render(self.game_map, self.player, self.enemies, self.items, self.current_floor, self.message, self.battle_log, self.chests)
            self.message = ""

            if not self.player.is_alive():
                self.save_data['deaths'] += 1
                self.update_playtime_and_save()
                self.stdscr.clear()
                cause = "YOU DIED" 
                if self.player.hunger <= 0: cause = "YOU STARVED TO DEATH"
                self.stdscr.addstr(self.map_height // 2, self.map_width // 2 - len(cause)//2, cause)
                self.stdscr.refresh()
                self.stdscr.getch()
                return "dead"

            key = self.stdscr.getch()
            
            # --- ЛОГИКА ПОДТВЕРЖДЕНИЯ ВЫХОДА ---
            if self.awaiting_quit_confirm:
                if key == 27: # 27 - это код клавиши ESC в curses
                    exit() # Подтвердили выход
                else:
                    self.awaiting_quit_confirm = False # Отменили выход любой другой клавишей
                    self.message = "Quit cancelled."
                    continue # Пропускаем дальнейшую обработку этого нажатия

            # --- ЛОГИКА АТАКИ В НАПРАВЛЕНИИ ---
            if self.awaiting_attack_direction:
                dx, dy = 0, 0
                if key == curses.KEY_UP or key == ord('w'): dy = -1
                elif key == curses.KEY_DOWN or key == ord('s'): dy = 1
                elif key == curses.KEY_LEFT or key == ord('a'): dx = -1
                elif key == curses.KEY_RIGHT or key == ord('d'): dx = 1
                # Диагональные направления из настроек
                elif key == self.keybindings.get('move_nw'): dx, dy = -1, -1
                elif key == self.keybindings.get('move_ne'): dx, dy = 1, -1
                elif key == self.keybindings.get('move_sw'): dx, dy = -1, 1
                elif key == self.keybindings.get('move_se'): dx, dy = 1, 1
                
                if dx != 0 or dy != 0:
                    command = AttackCommand(self.player, dx, dy, self)
                    command.execute()
                
                self.awaiting_attack_direction = False
                self.message = ""
                continue

            # --- ИНИЦИАЦИЯ ВЫХОДА ---
            if key == ord('q'):
                self.awaiting_quit_confirm = True
                self.message = "Are you sure you want to quit the game? (press ESC to confirm)"
                continue # Переходим к следующему кадру, чтобы показать сообщение
            
            # Вызов инвентаря
            if key == ord('i') and not self.awaiting_open_direction:
                Menu(self.stdscr).inventory_menu(self.player, self)
                continue 

            # Логика ожидания направления для открытия двери
            if self.awaiting_open_direction:
                dx, dy = 0, 0
                if key == curses.KEY_UP or key == ord('w'): dy = -1
                elif key == curses.KEY_DOWN or key == ord('s'): dy = 1
                elif key == curses.KEY_LEFT or key == ord('a'): dx = -1
                elif key == curses.KEY_RIGHT or key == ord('d'): dx = 1
                
                if dx != 0 or dy != 0:
                    tx, ty = self.player.x + dx, self.player.y + dy
                    if 0 <= tx < self.game_map.width and 0 <= ty < self.game_map.height:
                        
                        # 1. Попытка открыть дверь
                        if self.game_map.tiles[ty][tx] == '+':
                            self.game_map.tiles[ty][tx] = '/'
                            self.game_map.explored[ty][tx] = False
                            self.game_map.reveal_area(tx, ty)
                            self.wake_enemies_in_explored()
                            self.message = "You opened the door."
                        
                        # 2. Попытка открыть сундук
                        else:
                            target_chest = next((c for c in self.chests if c['x'] == tx and c['y'] == ty), None)
                            if target_chest:
                                # Генерация лута при ПЕРВОМ открытии
                                if not target_chest['opened']:
                                    target_chest['opened'] = True
                                    loot = self.generate_chest_loot()
                                    # Сразу добавляем предметы на пол под сундуком
                                    for item in loot:
                                        item.x, item.y = tx, ty
                                        self.items.append(item)
                                    self.message = "You opened the chest!"
                                else:
                                    self.message = "You look inside the chest..."
                                
                                # Проверяем, есть ли предметы на клетке сундука (для любого открытия)
                                items_here = [i for i in self.items if i.x == tx and i.y == ty]
                                if items_here:
                                    picked_indices = Menu(self.stdscr).loot_menu(items_here)
                                    
                                    for index in sorted(picked_indices, reverse=True):
                                        item = items_here[index]
                                        if self.player.add_item(item):
                                            self.items.remove(item)
                                            self.message += f" Picked up {item.name}."
                                else:
                                    self.message += " It is empty."
                            else:
                                self.message = "You can't open that."
                else:
                    self.message = "Cancelled."
                
                self.awaiting_open_direction = False
                continue

            command = self.handle_input(key)

            if command:
                if isinstance(command, WaitCommand):
                    self.player.process_regen()
                else:
                    command.execute()
                
                # --- Система голода ---
                self.turn_counter += 1
                enemies_alive = any(e.is_alive() for e in self.enemies)
                
                # Если врагов нет, голод уменьшается в 2 раза медленнее (каждый 2-й ход)
                should_tick_hunger = True
                if not enemies_alive and self.turn_counter % 2 != 0:
                    should_tick_hunger = False
                
                if should_tick_hunger:
                    self.player.tick_hunger()

                self.handle_enemy_deaths()

                self.player_actions_taken += 1
                actions_per_tick = 2 if self.player.dex_stat >= 5 else 1
                
                if self.player_actions_taken >= actions_per_tick:
                    self.player_actions_taken = 0
                    for enemy in self.enemies[:]:
                        if enemy.is_alive() and not enemy.is_turn_consumed:
                            enemy_command = enemy.ai.get_action(enemy, self.game_map, self.player, self.enemies)
                            if enemy_command:
                                enemy_command.execute()
                    self.handle_enemy_deaths()
                    for enemy in self.enemies:
                        enemy.is_turn_consumed = False

    def handle_input(self, key):
        is_free_attack = (self.player.dex_stat >= 5 and self.player_actions_taken == 1)

        if key == curses.KEY_UP or key == ord('w'):
            return MoveCommand(self.player, 0, -1, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == curses.KEY_DOWN or key == ord('s'):
            return MoveCommand(self.player, 0, 1, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == curses.KEY_LEFT or key == ord('a'):
            return MoveCommand(self.player, -1, 0, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == curses.KEY_RIGHT or key == ord('d'):
            return MoveCommand(self.player, 1, 0, self.game_map, self.player, self.enemies, is_free_attack)
        
        # Диагональное движение (из настроек)
        elif key == self.keybindings.get('move_nw'):
            return MoveCommand(self.player, -1, -1, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == self.keybindings.get('move_ne'):
            return MoveCommand(self.player, 1, -1, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == self.keybindings.get('move_sw'):
            return MoveCommand(self.player, -1, 1, self.game_map, self.player, self.enemies, is_free_attack)
        elif key == self.keybindings.get('move_se'):
            return MoveCommand(self.player, 1, 1, self.game_map, self.player, self.enemies, is_free_attack)
        # Клавиша F (Fire/Force)
        elif key == ord('f'):
            self.awaiting_attack_direction = True
            self.message = "Attack in which direction? (W/A/S/D)"
            return None    
        # Ctrl + WASD (Прямые комбинации для надежности)
        elif key == 23: # Ctrl + W
            return AttackCommand(self.player, 0, -1, self)
        elif key == 19: # Ctrl + S
            return AttackCommand(self.player, 0, 1, self)
        elif key == 1:  # Ctrl + A
            return AttackCommand(self.player, -1, 0, self)
        elif key == 4:  # Ctrl + D
            return AttackCommand(self.player, 1, 0, self)
        elif key == ord('e'):
            return WaitCommand()
        elif key == ord('v'):
            return DescendCommand(self.player, self.game_map, self)
        elif key == ord('g'): # Кнопка подбора предметов
            return GetCommand(self)
        elif key == ord('o'):
            self.awaiting_open_direction = True
            self.message = "What do you want to open? (Direction)"
            return None
        return None