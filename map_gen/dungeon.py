import random
import time
import heapq
from collections import deque
from actors.enemy import Rat, Goblin, Skeleton
from items.item import Item

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    # Отступ в 3 клетки гарантирует, что между любыми комнатами будет толстая стена
    def intersect(self, other):
        return (self.x1 - 3 <= other.x2 and self.x2 + 3 >= other.x1 and
                self.y1 - 3 <= other.y2 and self.y2 + 3 >= other.y1)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Изначально вся карта — это глухая стена (#)
        self.tiles = [['#' for _ in range(width)] for _ in range(height)]
        self.explored = [[False for _ in range(width)] for _ in range(height)]

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] in ['.', ':', 'L', '/'] # + закрытая дверь тоже проходима для логики (пока не добавим блокировку)
        return False

    def reveal_area(self, start_x, start_y):
        queue = deque([(start_x, start_y)])
        
        while queue:
            x, y = queue.popleft()
            
            if not (0 <= x < self.width and 0 <= y < self.height):
                continue
            if self.explored[y][x]:
                continue
            if self.tiles[y][x] == '#':
                continue
            
            # Двери видим, но сквозь них не просматриваем
            if self.tiles[y][x] == '+':
                self.explored[y][x] = True
                continue
            
            self.explored[y][x] = True
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.tiles[ny][nx] == '#':
                            self.explored[ny][nx] = True # Подсвечиваем стены вокруг
                        elif self.tiles[ny][nx] == '+':
                            self.explored[ny][nx] = True
                        elif not self.explored[ny][nx] and self.tiles[ny][nx] not in ['+', '#']:
                            queue.append((nx, ny))

def generate_dungeon(map_width, map_height, player_x=None, player_y=None, first_floor=True, current_floor=1):
    random.seed(time.time())
    MARGIN = 4
    
    game_map = GameMap(map_width, map_height)
    rooms = []
    target_rooms = random.randint(4, 9)
    
    # Обработка спуска на новый этаж
    if not first_floor and player_x is not None and player_y is not None:
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        x1 = random.randint(max(MARGIN, player_x - w + 1), min(player_x, map_width - MARGIN - w))
        y1 = random.randint(max(MARGIN, player_y - h + 1), min(player_y, map_height - MARGIN - h))
        start_room = Rect(x1, y1, w, h)
        
        for i in range(start_room.x1, start_room.x2):
            for j in range(start_room.y1, start_room.y2):
                game_map.tiles[j][i] = '.'
                
        rooms.append(start_room)

    # Генерация комнат
    for _ in range(100):
        if len(rooms) >= target_rooms:
            break
            
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        x = random.randint(MARGIN, map_width - w - MARGIN)
        y = random.randint(MARGIN, map_height - h - MARGIN)
        
        new_room = Rect(x, y, w, h)
        
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        
        if not failed:
            for i in range(new_room.x1, new_room.x2):
                for j in range(new_room.y1, new_room.y2):
                    game_map.tiles[j][i] = '.'
            rooms.append(new_room)

    # АЛГОРИТМ МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА (Prim's MST)
    # Гарантирует, что все комнаты соединены, но без лишних пересечений
    if len(rooms) > 1:
        in_mst = [False] * len(rooms)
        edges = []
        in_mst[0] = True
        
        # Добавляем ребра от первой комнаты
        cx0, cy0 = rooms[0].center()
        for j in range(1, len(rooms)):
            cxj, cyj = rooms[j].center()
            dist = abs(cx0 - cxj) + abs(cy0 - cyj)
            heapq.heappush(edges, (dist, 0, j))
            
        while edges:
            dist, i, j = heapq.heappop(edges)
            if not in_mst[j]:
                in_mst[j] = True
                # Соединяем комнату i и j
                _carve_corridor(game_map, rooms[i].center(), rooms[j].center())
                
                # Добавляем новые ребра от комнаты j
                cxj, cyj = rooms[j].center()
                for k in range(len(rooms)):
                    if not in_mst[k]:
                        cxk, cyk = rooms[k].center()
                        d = abs(cxj - cxk) + abs(cyj - cyk)
                        heapq.heappush(edges, (d, j, k))

    # РАССТАНОВКА ДВЕРЕЙ 
    # Ищем стены, которые разделяют пол комнаты (.) и пол коридора (:)
    for y in range(1, map_height - 1):
        for x in range(1, map_width - 1):
            if game_map.tiles[y][x] == '#':
                # Горизонтальная дверь (стены сверху и снизу)
                if game_map.tiles[y-1][x] == '#' and game_map.tiles[y+1][x] == '#':
                    left = game_map.tiles[y][x-1]
                    right = game_map.tiles[y][x+1]
                    if (left == '.' and right == ':') or (left == ':' and right == '.'):
                        game_map.tiles[y][x] = '+'
                # Вертикальная дверь (стены слева и справа)
                elif game_map.tiles[y][x-1] == '#' and game_map.tiles[y][x+1] == '#':
                    up = game_map.tiles[y-1][x]
                    down = game_map.tiles[y+1][x]
                    if (up == '.' and down == ':') or (up == ':' and down == '.'):
                        game_map.tiles[y][x] = '+'

    # Спавн врагов и предметов
    enemies = []
    items = []
    if len(rooms) > 1:
        goblin_room_index = random.randint(1, len(rooms) - 1)
    else:
        goblin_room_index = -1
    
    for i, room in enumerate(rooms[1:]):
        room_index = i + 1
        
        if room_index == goblin_room_index:
            rx = random.randint(room.x1 + 1, room.x2 - 2)
            ry = random.randint(room.y1 + 1, room.y2 - 2)
            if game_map.tiles[ry][rx] == '.':
                enemies.append(Goblin(rx, ry))
        else:
            if random.random() < 0.6:
                num_rats = random.randint(1, 2)
                for _ in range(num_rats):
                    rx = random.randint(room.x1 + 1, room.x2 - 2)
                    ry = random.randint(room.y1 + 1, room.y2 - 2)
                    if game_map.tiles[ry][rx] == '.':
                        enemies.append(Rat(rx, ry))
            elif random.random() < 0.3:
                rx = random.randint(room.x1 + 1, room.x2 - 2)
                ry = random.randint(room.y1 + 1, room.y2 - 2)
                if game_map.tiles[ry][rx] == '.':
                    enemies.append(Skeleton(rx, ry))

    # --- СПАВН СУНДУКОВ ---
    chests = []
    if current_floor % 2 == 0 and len(rooms) > 1:
        # Выбираем случайную комнату, но не стартовую
        room_idx = random.randint(1, len(rooms) - 1)
        room = rooms[room_idx]
        cx = random.randint(room.x1 + 1, room.x2 - 2)
        cy = random.randint(room.y1 + 1, room.y2 - 2)
        if game_map.tiles[cy][cx] == '.':
            chests.append({'x': cx, 'y': cy, 'opened': False})

    if first_floor:
        player_x, player_y = rooms[0].center()
    
    stairs_x, stairs_y = rooms[-1].center()
    game_map.tiles[stairs_y][stairs_x] = 'L'

    game_map.reveal_area(player_x, player_y)

    return game_map, player_x, player_y, enemies, items, chests

# Вспомогательная функция вырезания L-образного коридора
def _carve_corridor(game_map, start, end):
    x1, y1 = start
    x2, y2 = end
    
    if random.random() < 0.5:
        _carve_horizontal_line(game_map, x1, x2, y1)
        _carve_vertical_line(game_map, y1, y2, x2)
    else:
        _carve_vertical_line(game_map, y1, y2, x1)
        _carve_horizontal_line(game_map, x1, x2, y2)

def _carve_horizontal_line(game_map, x1, x2, y):
    step = 1 if x2 > x1 else -1
    entered_wall = False
    last_wall_x, last_wall_y = -1, -1
    
    for x in range(x1, x2 + step, step):
        tile = game_map.tiles[y][x]
        
        if tile == '#':
            game_map.tiles[y][x] = ':' # Вырезаем коридор
            entered_wall = True
            last_wall_x, last_wall_y = x, y # Запоминаем последнюю вырезанную стену
        elif tile == '.' or tile == ':':
            if entered_wall:
                # МЫ ТОЛЬКО ЧТО ВОШЛИ В КОМНАТУ ИЛИ ЧУЖОЙ КОРИДОР!
                # Гарантированно ставим дверь на границе (там, где была последняя стена)
                if 0 <= last_wall_y < game_map.height and 0 <= last_wall_x < game_map.width:
                    # Проверяем, что это узкий проем (стены сверху и снизу), чтобы дверь выглядела логично
                    above = game_map.tiles[last_wall_y-1][last_wall_x] if last_wall_y > 0 else '#'
                    below = game_map.tiles[last_wall_y+1][last_wall_x] if last_wall_y < game_map.height-1 else '#'
                    if above == '#' and below == '#':
                        game_map.tiles[last_wall_y][last_wall_x] = '+'
                return # Останавливаем вырезание, чтобы не портить комнату

def _carve_vertical_line(game_map, y1, y2, x):
    step = 1 if y2 > y1 else -1
    entered_wall = False
    last_wall_x, last_wall_y = -1, -1
    
    for y in range(y1, y2 + step, step):
        tile = game_map.tiles[y][x]
        
        if tile == '#':
            game_map.tiles[y][x] = ':'
            entered_wall = True
            last_wall_x, last_wall_y = x, y
        elif tile == '.' or tile == ':':
            if entered_wall:
                if 0 <= last_wall_y < game_map.height and 0 <= last_wall_x < game_map.width:
                    left = game_map.tiles[last_wall_y][last_wall_x-1] if last_wall_x > 0 else '#'
                    right = game_map.tiles[last_wall_y][last_wall_x+1] if last_wall_x < game_map.width-1 else '#'
                    if left == '#' and right == '#':
                        game_map.tiles[last_wall_y][last_wall_x] = '+'
                return