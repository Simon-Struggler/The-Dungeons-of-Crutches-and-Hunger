import curses

class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def render(self, game_map, player, enemies, items, current_floor, message, battle_log, chests):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # UI строка 0 и 1 сверху
        key_str = "[Key]" if player.has_key() else ""
        ui_line1 = f"Floor:{current_floor} Lv:{player.level} HP:{player.hp}/{player.max_hp} ATK:{player.get_attack_power()} {key_str}"
        self.stdscr.addstr(0, 1, ui_line1)
        hunger_str = player.get_hunger_status()
        str_b = player.get_total_str() - player.str_stat
        dex_b = player.get_total_dex() - player.dex_stat
        con_b = player.get_total_con() - player.con_stat
        
        str_str = f"STR:{player.str_stat}(+{str_b})" if str_b > 0 else f"STR:{player.str_stat}"
        dex_str = f"DEX:{player.dex_stat}(+{dex_b})" if dex_b > 0 else f"DEX:{player.dex_stat}"
        con_str = f"CON:{player.con_stat}(+{con_b})" if con_b > 0 else f"CON:{player.con_stat}"
        
        ui_line2 = f"{str_str} {dex_str} {con_str} | XP:{player.xp}/{player.xp_to_next_level()} | {hunger_str}"
        self.stdscr.addstr(1, 1, ui_line2)
        self.stdscr.addstr(1, 1, ui_line2)

        # --- РАМКИ КАРТЫ ---
        map_w = game_map.width
        map_h = game_map.height
        
        # Горизонтальные границы '_'
        for x in range(map_w + 2):
            self.stdscr.addch(2, x, '_')
            self.stdscr.addch(map_h + 3, x, '_')
        # Вертикальные границы '|'
        for y in range(2, map_h + 3):
            self.stdscr.addch(y, 0, '|')
            self.stdscr.addch(y, map_w + 1, '|')

        # --- ОТРИСОВКА КАРТЫ (со смещением +1 по X и +3 по Y) ---
        for y in range(game_map.height):
            for x in range(game_map.width):
                draw_x = x + 1
                draw_y = y + 3
                
                if draw_y < height and draw_x < width:
                    if not game_map.explored[y][x]:
                        self.stdscr.addch(draw_y, draw_x, ' ')
                    else:
                        tile = game_map.tiles[y][x]
                        if tile == ':': char_to_draw = ' '
                        elif tile == '+': char_to_draw = '+'
                        elif tile == '/': char_to_draw = '/'
                        else: char_to_draw = tile
                        self.stdscr.addch(draw_y, draw_x, char_to_draw)

        # Предметы
        # 1. СНАЧАЛА Отрисовываем предметы (они могут лежать на клетке)
        floor_items = {}
        for item in items:
            if game_map.explored[item.y][item.x]:
                pos = (item.x, item.y)
                if pos not in floor_items: floor_items[pos] = []
                floor_items[pos].append(item)

        for (ix, iy), item_list in floor_items.items():
            draw_x, draw_y = ix + 1, iy + 3
            if draw_y < height and draw_x < width and game_map.explored[iy][ix]:
                char = 'I' if len(item_list) > 1 else item_list[0].char
                self.stdscr.addch(draw_y, draw_x, char)

        # 2. ПОСЛЕ Отрисовка сундуков (перекрывает иконки предметов, если они лежат в сундуке)
        for chest in chests:
            if game_map.explored[chest['y']][chest['x']]:
                draw_x, draw_y = chest['x'] + 1, chest['y'] + 3
                if draw_y < height and draw_x < width:
                    self.stdscr.addch(draw_y, draw_x, 'c')

        # Враги
        for enemy in enemies:
            draw_x, draw_y = enemy.x + 1, enemy.y + 3
            if enemy.is_alive() and game_map.explored[enemy.y][enemy.x] and draw_y < height and draw_x < width:
                self.stdscr.addch(draw_y, draw_x, enemy.char)

        # Игрок
        draw_x, draw_y = player.x + 1, player.y + 3
        if draw_y < height and draw_x < width:
            self.stdscr.addch(draw_y, draw_x, player.char)

        # --- BATTLE LOG (Справа от карты) ---
        log_x = map_w + 4 # Отступаем от правой рамки карты
        log_y_start = 2
        
        # Заголовок лога
        if log_x + 16 < width:
            self.stdscr.addstr(log_y_start, log_x, "--- COMBAT LOG ---", curses.A_BOLD)
        
        # Выводим последние строки лога, которые помещаются на экран
        max_log_display = height - log_y_start - 2
        start_idx = max(0, len(battle_log) - max_log_display)
        
        y_offset = 1
        for i in range(start_idx, len(battle_log)):
            if log_y_start + y_offset < height - 1:
                # Обрезаем слишком длинные строки, чтобы не вылезти за экран
                log_msg = battle_log[i][:width - log_x - 1]
                try:
                    self.stdscr.addstr(log_y_start + y_offset, log_x, log_msg)
                except curses.error:
                    pass
                y_offset += 1

        # Обычные сообщения (подбор предметов и т.д.)
        if message and map_h + 4 < height:
            self.stdscr.addstr(map_h + 4, 1, message)

        self.stdscr.refresh()