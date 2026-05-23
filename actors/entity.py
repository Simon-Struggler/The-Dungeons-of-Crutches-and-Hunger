import random

class Entity:
    def __init__(self, x: int, y: int, char: str, hp: int, base_attack: int, str_stat: int, dex_stat: int, con_stat: int, color=0):
        self.x = x
        self.y = y
        self.char = char
        self.color = color 
        self.base_attack = base_attack
        self.str_stat = str_stat
        self.dex_stat = dex_stat
        self.con_stat = con_stat
        
        self.max_hp = hp + ((self.con_stat - 1) * 2)
        self.hp = self.max_hp
        
        self.is_turn_consumed = False

    def is_alive(self):
        return self.hp > 0

    def get_attack_damage(self):
        """Вычисляет урон: от базового до базового + сила."""
        min_dmg = self.base_attack
        max_dmg = self.base_attack + self.str_stat
        return random.randint(min_dmg, max_dmg)

    def get_crit_chance(self):
        """Базовый шанс 1% + 3% за каждую единицу ловкости."""
        return 1 + (self.dex_stat * 3)

    def try_dodge(self):
        """Шанс уклонения: DEX * 5%."""
        dodge_chance = self.dex_stat * 5
        return random.randint(1, 100) <= dodge_chance

    def take_damage(self, amount, is_crit=False):
        """Получение урона с учетом защиты CON (5+ CON дает -1 к входящему урону)."""
        damage_reduction = 0
        if self.con_stat >= 5:
            damage_reduction = 1
            
        actual_damage = max(0, amount - damage_reduction)
        self.hp -= actual_damage
        return actual_damage
