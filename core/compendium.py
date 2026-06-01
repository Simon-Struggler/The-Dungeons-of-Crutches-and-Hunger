# Словари с описаниями. Ключ - имя класса (строго __name__), значение - словарь с char и description.
ENEMY_TEMPLATES = {
    "Rat": {"char": "r", "name": "Rat", "description": "A common, filthy rodent. More of a nuisance than a threat."},
    "AngryRat": {"char": "a", "name": "Angry Rat", "description": "A larger rat, maddened by hunger. It won't flee from you."},
    "Goblin": {"char": "G", "name": "Goblin Keymaster", "description": "A cunning green creature. Always carries a key to the lower levels."},
    "Skeleton": {"char": "S", "name": "Skeleton", "description": "Animated bones held together by dark magic. Carries rusty equipment."},
    "Knight": {"char": "K", "name": "Dungeon Knight", "description": "An armored sentinel. Slow to anger, but hits hard."},
    "Zombie": {"char": "z", "name": "Zombie", "description": "A shambling corpse. Slow, but relentless in its pursuit of flesh."},
    "Lizardman": {"char": "Z", "name": "Lizardman", "description": "A reptilian warrior wielding curved swords. Quick and deadly."},
    "Construct": {"char": "C", "name": "Construct", "description": "A mechanical guardian powered by Life Gems. Does not actively pursue, but holds its ground."},
    "Phantasm": {"char": "P", "name": "Phantasm", "description": "A ghostly apparition. Its touch drains the life essence."},
    "Whight": {"char": "W", "name": "Whight", "description": "A powerful undead sorcerer. Commands frost and dark magic."},
    "Quazimorph": {"name": "Q", "char": "Quazimorph", "description": "An eldritch horror from the deepest abyss. Defies logic and sanity."},
    "RatKing": {"char": "R", "name": "Rat King", "description": "A bloated mass of rats twisted into one crowned entity."},
    "DeathKnight": {"char": "D", "name": "Death Knight", "description": "A fallen champion bound to the dungeon. Wields the dreaded Soul Reaper."},
    "Nightmare": {"char": "N", "name": "Nightmare", "description": "The immortal ruler of the lowest depths. Seek the White Mask to end its reign... or continue it."}
}

ITEM_TEMPLATES = {
    "RatMeat": {"char": "m", "name": "Rat Meat", "description": "Tough and hairy. Recovers 4 HP and 100 Hunger."},
    "DungeonKey": {"char": "k", "name": "Dungeon Key", "description": "Opens the hatch to descend deeper."},
    "OldSword": {"char": "!", "name": "Old Sword", "description": "A dull iron sword. +1 Min Damage."},
    "CurvedSword": {"char": ")", "name": "Curved Sword", "description": "A steel curved sword. +2 Min Damage."},
    "SoulReaper": {"char": "?", "name": "Soul Reaper", "description": "Death Knight's scythe. +3 Min Damage, 15% Crit, 2-Handed, Ranged."},
    "WhiteMask": {"char": "w", "name": "White Mask", "description": "An expressionless porcelain mask. +3 All Stats, -1 Dmg Taken. Story ending item."},
    "HatOfKnowledge": {"char": "h", "name": "Hat of Knowledge", "description": "Increases XP gained from kills by 1."},
    "Glasses": {"char": "g", "name": "Glasses", "description": "Increases Critical Hit chance by 15%."},
    "Chainmail": {"char": "M", "name": "Chainmail", "description": "Reduces all incoming attack damage by 1."},
    "GlovesOfDexterity": {"char": "d", "name": "Gloves of Dexterity", "description": "Increases Dexterity by 1."},
    "Spear": {"char": "^", "name": "Spear", "description": "+1 Min Damage. 2-Handed. Can attack 1 tile away."},
    "Buckler": {"char": "b", "name": "Buckler", "description": "30% chance to block normal damage."},
    "LeggingsOfStrength": {"char": "U", "name": "Leggings of Strength", "description": "Increases Strength by 1."},
    "AchillesSandals": {"char": "A", "name": "Achilles Sandals", "description": "Increases Maximum HP by 10."},
    "LifeGem": {"char": "*", "name": "Life Gem", "description": "Recovers 15 HP."},
    "PotionOfHealing": {"char": "h", "name": "Potion of Healing", "description": "Recovers 30 HP and 150 Hunger."}
}