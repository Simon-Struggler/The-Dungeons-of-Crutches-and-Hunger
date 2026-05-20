import abc
from actors.player import Player

class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass

class WaitCommand(Command):
    def execute(self):
        pass

class MoveCommand(Command):
    def __init__(self, entity, dx: int, dy: int, game_map, player=None, enemies=None, is_free_attack=False, ignore_walls=False):
        self.entity = entity
        self.dx = dx
        self.dy = dy
        self.game_map = game_map
        self.player = player
        self.enemies = enemies if enemies is not None else []
        self.is_free_attack = is_free_attack
        self.ignore_walls = ignore_walls # Новый флаг

    def execute(self):
        new_x = self.entity.x + self.dx
        new_y = self.entity.y + self.dy
        
        # Передаем флаг ignore_walls
        if not self.game_map.is_walkable(new_x, new_y, self.ignore_walls):
            return

        if isinstance(self.entity, Player):
            target_enemy = None
            for e in self.enemies:
                if e.is_alive() and e.x == new_x and e.y == new_y:
                    target_enemy = e
                    break
            
            if target_enemy:
                target_enemy.is_turn_consumed = True
                survived = self.entity.engine_ref.resolve_attack(self.entity, target_enemy)
                if survived and not self.is_free_attack:
                    self.entity.engine_ref.resolve_attack(target_enemy, self.entity)
                    self.entity.reset_regen()
            else:
                self.entity.x = new_x
                self.entity.y = new_y
                self.entity.reset_regen()

        else:
            # Логика врага
            if self.player and self.player.x == new_x and self.player.y == new_y:
                from strategies.ai_behavior import MediumAggressiveAI, ShortAggressiveAI
                if isinstance(self.entity.ai, MediumAggressiveAI):
                    survived = self.entity.engine_ref.resolve_attack(self.entity, self.player)
                    self.entity.is_turn_consumed = True
                    if survived:
                        self.entity.engine_ref.resolve_attack(self.player, self.entity)
                        self.player.reset_regen()
                elif isinstance(self.entity.ai, ShortAggressiveAI):
                    survived = self.entity.engine_ref.resolve_attack(self.entity, self.player)
                    self.entity.is_turn_consumed = True
                    if survived:
                        self.entity.engine_ref.resolve_attack(self.player, self.entity)
                        self.player.reset_regen()
                return
            
            for e in self.enemies:
                if e is not self.entity and e.is_alive() and e.x == new_x and e.y == new_y:
                    return

            self.entity.x = new_x
            self.entity.y = new_y

class AttackCommand(Command):
    def __init__(self, entity, dx, dy, engine):
        self.entity = entity
        self.dx = dx
        self.dy = dy
        self.engine = engine

    def execute(self):
        player = self.entity
        has_spear = any(item.ranged for item in player.equipment.values() if item)
        
        # Проверяем врага на расстоянии 2 клеток (для копья)
        target_range2 = None
        if has_spear:
            tx2, ty2 = player.x + self.dx * 2, player.y + self.dy * 2
            for e in self.engine.enemies:
                if e.is_alive() and e.x == tx2 and e.y == ty2:
                    target_range2 = e
                    break
        
        # Проверяем врага на расстоянии 1 клетки (соседняя)
        tx1, ty1 = player.x + self.dx, player.y + self.dy
        target_range1 = None
        for e in self.engine.enemies:
            if e.is_alive() and e.x == tx1 and e.y == ty1:
                target_range1 = e
                break
        
        # Приоритет: если есть копье и враг в 2 клетках, бьем вдаль. Иначе бьем вблизи.
        if target_range2:
            self.engine.resolve_attack(player, target_range2)
            # Без контратаки! Враг просто сделает свой ход (подойдет ближе) в фазе ИИ.
        elif target_range1:
            survived = self.engine.resolve_attack(player, target_range1)
            if survived:
                self.engine.resolve_attack(target_range1, player)
                player.reset_regen()
        else:
            self.engine.add_log("You swing at the air.")

class GetCommand(Command):
    def __init__(self, engine):
        self.engine = engine
    def execute(self):
        self.engine.handle_get()

class DescendCommand(Command):
    def __init__(self, entity, game_map, engine):
        self.entity = entity
        self.game_map = game_map
        self.engine = engine

    def execute(self):
        if self.game_map.tiles[self.entity.y][self.entity.x] == 'L':
            key_item = next((item for item in self.entity.inventory if item.name == "Dungeon Key"), None)
            if key_item:
                self.entity.inventory.remove(key_item)
                self.entity.reset_regen()
                self.engine.go_downstairs()
            else:
                self.engine.message = "You need a key to descend!"
