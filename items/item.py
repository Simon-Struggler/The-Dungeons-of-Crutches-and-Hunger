class Item:
    def __init__(self, x, y, name, char, category, description, max_stack=1, quantity=1, slot=None, 
                 attack_bonus=0, sub_category=None, nutrition_value=0, 
                 xp_bonus=0, crit_bonus=0, dmg_reduction=0, stat_bonuses=None, 
                 two_handed=False, ranged=False, block_chance=0, max_hp_bonus=0):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.category = category
        self.description = description
        self.max_stack = max_stack
        self.quantity = quantity
        self.slot = slot
        self.attack_bonus = attack_bonus
        self.sub_category = sub_category
        self.nutrition_value = nutrition_value
        
        # Новые свойства
        self.xp_bonus = xp_bonus                 # Hat of knowledge
        self.crit_bonus = crit_bonus             # Glasses
        self.dmg_reduction = dmg_reduction       # Chainmail
        self.stat_bonuses = stat_bonuses if stat_bonuses else {'str': 0, 'dex': 0, 'con': 0} # Gloves/Leggings
        self.two_handed = two_handed             # Spear
        self.ranged = ranged                     # Spear
        self.block_chance = block_chance         # Buckler
        self.max_hp_bonus = max_hp_bonus         # Achilles sandals

class RatMeat(Item):
    def __init__(self, x, y, quantity=1):
        super().__init__(x, y, name="Rat Meat", char='m', category='consumable', 
                         description="This is meat from a rat. It's tough, hairy and not very nutricious. Don't know what you expected. Recovers 4 HP and 75 Hunger on use.",
                         max_stack=10, quantity=quantity, sub_category='food', nutrition_value=75)

class DungeonKey(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Dungeon Key", char='k', category='key', 
                         description="It's an old metal key. You need this to open the hatch to the lower level. Goblins keymasters carry it. Use 'v' on an 'L' tile to descend.",
                         max_stack=1, quantity=1)

class OldSword(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Old Sword", char='s', category='equipment', 
                         description="It's a somewhat dull iron sword, carried by Skeletons. Not the best but it still beats bare fists. Equipping it grants +1 base damage",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=1)

# --- НОВАЯ ЭКИПИРОВКА ---

class HatOfKnowledge(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Hat of Knowledge", char='h', category='equipment',
                         description="A worn wizard hat. You hear faint whispers of old wisdom while wearing it. Increases XP gained from kills by 1.",
                         max_stack=1, quantity=1, slot='head', xp_bonus=1)

class Glasses(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Glasses", char='g', category='equipment',
                         description="A pair of lenses on a frame. You don't know what's more surprising - it being able to help with both nearsightedness and farsightedness or that there isn't a scratch on the lenses. Increases Critical Hit chance by 15%.",
                         max_stack=1, quantity=1, slot='face', crit_bonus=15)

class Chainmail(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Chainmail", char='M', category='equipment',
                         description="Hundreds of iron rings woven together. It's both heavier and lighter than you expected. Reduces all incoming attack damage by 1.",
                         max_stack=1, quantity=1, slot='chest', dmg_reduction=1)

class GlovesOfDexterity(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Gloves of Dexterity", char='d', category='equipment',
                         description="A pair of sleek leather gloves. Besides looking fashionable, they make you feel lighter. Increases Dexterity by 1.",
                         max_stack=1, quantity=1, slot='hands', stat_bonuses={'str': 0, 'dex': 1, 'con': 0})

class Spear(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Spear", char='^', category='equipment',
                         description="A long wooden shaft with a metal tip. Two-handed. +1 minimum Damage. Can attack enemies 1 tile away.",
                         max_stack=1, quantity=1, slot='main_hand', attack_bonus=1, two_handed=True, ranged=True)

class Buckler(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Buckler", char='b', category='equipment',
                         description="A small metal shield. 30% chance to completely block normal damage. Critical hits bypass block but deal normal damage instead.",
                         max_stack=1, quantity=1, slot='off_hand', block_chance=30)

class LeggingsOfStrength(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Leggings of Strength", char='U', category='equipment',
                         description="A pair of leather pants. Not the best in the protection department but wearing them makes you feel... Stronger. Increases Strength by 1.",
                         max_stack=1, quantity=1, slot='legs', stat_bonuses={'str': 1, 'dex': 0, 'con': 0})

class AchillesSandals(Item):
    def __init__(self, x, y):
        super().__init__(x, y, name="Achilles Sandals", char='A', category='equipment',
                         description="A pair of old sandals with buckles of tarnished gold. Wearing them makes you feel a little less vincible. Increases Maximum HP by 10 while equipped.",
                         max_stack=1, quantity=1, slot='feet', max_hp_bonus=10)