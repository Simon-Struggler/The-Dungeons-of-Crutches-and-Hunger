from ui.colors import COLOR_PAIR_RED, COLOR_PAIR_GREEN, COLOR_PAIR_CYAN, COLOR_PAIR_MAGENTA, COLOR_PAIR_YELLOW, COLOR_PAIR_BLUE, COLOR_PAIR_WHITE

class Item:
    def __init__(self, x, y, name, char, category, description, max_stack=1, quantity=1, slot=None, 
                 attack_bonus=0, sub_category=None, nutrition_value=0, hp_value=0, color=0,
                 xp_bonus=0, crit_bonus=0, dmg_reduction=0, stat_bonuses=None, 
                 two_handed=False, ranged=False, block_chance=0, max_hp_bonus=0):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color 
        self.category = category
        self.description = description
        self.max_stack = max_stack
        self.quantity = quantity
        self.slot = slot
        self.attack_bonus = attack_bonus
        self.sub_category = sub_category
        self.nutrition_value = nutrition_value
        self.hp_value = hp_value
        
        self.xp_bonus = xp_bonus
        self.crit_bonus = crit_bonus
        self.dmg_reduction = dmg_reduction
        self.stat_bonuses = stat_bonuses if stat_bonuses else {'str': 0, 'dex': 0, 'con': 0}
        self.two_handed = two_handed
        self.ranged = ranged
        self.block_chance = block_chance
        self.max_hp_bonus = max_hp_bonus

class RatMeat(Item):
    def __init__(self, x, y, quantity=1):
        super().__init__(x, y, name="Rat Meat", char='m', category='consumable', 
                         description="Recovers 4 HP and 100 Hunger on use.",
                         max_stack=10, quantity=quantity, sub_category='food', nutrition_value=100, hp_value=4, color=COLOR_PAIR_RED)

class DungeonKey(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Dungeon Key", char='k', category='key', 
                         description="Use 'v' on an 'L' tile to descend.",
                         max_stack=1, quantity=1, color=COLOR_PAIR_YELLOW)

class OldSword(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Old Sword", char='!', category='equipment', 
                         description="A dull iron sword. +1 Min Damage",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=1)

class CurvedSword(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Curved Sword", char=')', category='equipment', 
                         description="It's a steel curved sword, carried by Lizardmen. A solid weapon. Equipping it grants +2 base damage",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=2, color=COLOR_PAIR_CYAN)

class SoulReaper(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Soul Reaper", char='?', category='equipment', 
                         description="It's the scythe that the Death Knight carried. Heavy and long, with a blade so sharp it can cut the life essence of your enemies. Equipping it grants +4 base damage and 25% crit rate.",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=3, crit_bonus=15, two_handed=True, ranged=True, color=COLOR_PAIR_MAGENTA)

class WhiteMask(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="White Mask", char='w', category='equipment',
                         description="An expressionless porcelain white mask. Cannot be broken by any normal means. You have a sudden urge to put it on...",
                         max_stack=1, quantity=1, slot='face', stat_bonuses={'str': 3, 'dex': 3, 'con': 3}, dmg_reduction=1, color=COLOR_PAIR_WHITE)

class HatOfKnowledge(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Hat of Knowledge", char='h', category='equipment',
                         description="A worn wizard hat. Increases XP gained from kills by 1.",
                         max_stack=1, quantity=1, slot='head', xp_bonus=1)

class Glasses(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Glasses", char='g', category='equipment',
                         description="Thick lenses. Increases Critical Hit chance by 15%.",
                         max_stack=1, quantity=1, slot='face', crit_bonus=15)

class Chainmail(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Chainmail", char='M', category='equipment',
                         description="Heavy iron rings. Reduces all incoming attack damage by 1.",
                         max_stack=1, quantity=1, slot='chest', dmg_reduction=1)

class GlovesOfDexterity(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Gloves of Dexterity", char='d', category='equipment',
                         description="Silky gloves. Increases Dexterity by 1.",
                         max_stack=1, quantity=1, slot='hands', stat_bonuses={'str': 0, 'dex': 1, 'con': 0}, color=COLOR_PAIR_GREEN)

class Spear(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Spear", char='^', category='equipment',
                         description="A long wooden shaft with a tip. Two-handed. +1 Min Damage. Can attack enemies 1 tile away without retaliation.",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=1, two_handed=True, ranged=True)

class Buckler(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Buckler", char='b', category='equipment',
                         description="A small shield. 30% chance to completely block normal damage. Critical hits bypass block but deal normal damage instead.",
                         max_stack=1, quantity=1, slot='off_hand', block_chance=30)

class LeggingsOfStrength(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Leggings of Strength", char='U', category='equipment',
                         description="Sturdy leather pants. Increases Strength by 1.",
                         max_stack=1, quantity=1, slot='legs', stat_bonuses={'str': 1, 'dex': 0, 'con': 0})

class AchillesSandals(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Achilles Sandals", char='A', category='equipment',
                         description="Winged sandals. Increases Maximum HP by 10 while equipped.",
                         max_stack=1, quantity=1, slot='feet', max_hp_bonus=10, color=COLOR_PAIR_YELLOW)

class LifeGem(Item):
    def __init__(self, x, y, quantity=1):
        super().__init__(x, y, name="Life Gem", char='*', category='consumable', 
                         description="A magical crystal that grants Constructs life but not sentience. Break it to recover 15 HP.",
                         max_stack=10, quantity=quantity, sub_category='potion', hp_value=15, color=COLOR_PAIR_BLUE)

class PotionOfHealing(Item):
    def __init__(self, x, y, quantity=1):
        super().__init__(x, y, name="Potion of healing", char='h', category='consumable', 
                         description="A small glass vial with red liquid. Tastes like wine. Use them sparingly. Gives 30 HP and 150 Hunger on use",
                         max_stack=10, quantity=quantity, sub_category='potion', nutrition_value=150, hp_value=30, color=COLOR_PAIR_RED)
