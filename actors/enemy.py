from actors.entity import Entity
from strategies.ai_behavior import PassiveAI, SimpleAggressiveAI

class Rat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="r", hp=3, base_attack=1, str_stat=1, dex_stat=1, con_stat=1)
        self.ai = PassiveAI()
        self.xp_reward = 1

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