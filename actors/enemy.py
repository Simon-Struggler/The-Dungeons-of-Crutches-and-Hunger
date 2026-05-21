from actors.entity import Entity
from strategies.ai_behavior import PassiveAI, ShortAggressiveAI, MediumAggressiveAI

class Rat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="r", hp=3, base_attack=1, str_stat=1, dex_stat=1, con_stat=1)
        self.ai = PassiveAI()
        self.xp_reward = 1

class AngryRat(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="a", hp=12, base_attack=2, str_stat=2, dex_stat=2, con_stat=2)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 20

class Goblin(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="G", hp=5, base_attack=2, str_stat=1, dex_stat=4, con_stat=1)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 5

class Skeleton(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="S", hp=8, base_attack=2, str_stat=2, dex_stat=1, con_stat=1)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 10

class Knight(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="K", hp=25, base_attack=3, str_stat=2, dex_stat=2, con_stat=3)
        self.ai = ShortAggressiveAI()
        self.xp_reward = 50

class Zombie(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="z", hp=8, base_attack=1, str_stat=1, dex_stat=1, con_stat=2)
        self.ai = ShortAggressiveAI()
        self.xp_reward = 4

class Lizardman(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="Z", hp=18, base_attack=3, str_stat=2, dex_stat=3, con_stat=2)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 40

class Construct(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="C", hp=20, base_attack=2, str_stat=2, dex_stat=1, con_stat=2)
        self.ai = PassiveAI()
        self.xp_reward = 30 

class Phantasm(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="P", hp=20, base_attack=3, str_stat=9, dex_stat=3, con_stat=1)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 50

class Whight(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="W", hp=40, base_attack=4, str_stat=9, dex_stat=5, con_stat=3)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 100

class Quazimorph(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="Q", hp=60, base_attack=7, str_stat=7, dex_stat=4, con_stat=4)
        self.ai = ShortAggressiveAI()
        self.xp_reward = 250

class RatKing(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="R", hp=80, base_attack=2, str_stat=3, dex_stat=1, con_stat=3)
        self.ai = ShortAggressiveAI()
        self.xp_reward = 100

class DeathKnight(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="D", hp=50, base_attack=4, str_stat=5, dex_stat=2, con_stat=5)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 200

class Nightmare(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="N", hp=99, base_attack=6, str_stat=6, dex_stat=6, con_stat=6)
        self.ai = MediumAggressiveAI()
        self.xp_reward = 666
