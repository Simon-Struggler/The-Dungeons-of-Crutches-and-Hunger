from actors.entity import Entity
from strategies.ai_behavior import PassiveAI, SimpleAggressiveAI

class Rat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="r", hp=3, base_attack=1, str_stat=1, dex_stat=1, con_stat=1)
        self.ai = PassiveAI()
        self.xp_reward = 1

class AngryRat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="a", hp=8, base_attack=1, str_stat=2, dex_stat=2, con_stat=1)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 20

class Goblin(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="G", hp=5, base_attack=2, str_stat=1, dex_stat=4, con_stat=1)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 3

class Skeleton(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="S", hp=6, base_attack=2, str_stat=2, dex_stat=2, con_stat=1)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 4

class Lizardman(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="Z", hp=12, base_attack=3, str_stat=2, dex_stat=3, con_stat=1)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 30

class Construct(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="C", hp=15, base_attack=2, str_stat=1, dex_stat=1, con_stat=2)
        self.ai = PassiveAI()
        self.xp_reward = 30 

class Phantasm(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="P", hp=10, base_attack=1, str_stat=7, dex_stat=3, con_stat=1)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 40

class RatKing(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="R", hp=30, base_attack=2, str_stat=2, dex_stat=1, con_stat=2)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 60

class DeathKnight(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="D", hp=24, base_attack=2, str_stat=5, dex_stat=2, con_stat=2)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 160

class Nightmare(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="N", hp=33, base_attack=3, str_stat=3, dex_stat=3, con_stat=3)
        self.ai = SimpleAggressiveAI()
        self.xp_reward = 333
