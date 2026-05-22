import random
from actors.enemy import Rat, AngryRat, Goblin, Skeleton, Zombie, Lizardman, Construct, Phantasm, Whight, Knight, RatKing, DeathKnight, Nightmare, Quazimorph
from items.item import OldSword, CurvedSword, SoulReaper, WhiteMask, LifeGem, RatMeat, DungeonKey, Item, HatOfKnowledge, Glasses, Chainmail, GlovesOfDexterity, Spear, Buckler, LeggingsOfStrength, AchillesSandals, PotionOfHealing

class EnemyFactory:
    """Фабрика для создания врагов в зависимости от текущего этажа."""
    
    @staticmethod
    def spawn_boss(current_floor, x, y):
        if current_floor > 10: return Quazimorph(x, y)
        elif current_floor == 10: return Nightmare(x, y)
        elif current_floor == 8: return DeathKnight(x, y)
        elif current_floor == 6: return RatKing(x, y)
        elif current_floor >= 4: return Knight(x, y)
        else: return Goblin(x, y)

    @staticmethod
    def spawn_regular(current_floor, x, y):
        eligible = []
        if current_floor >= 10:
            eligible.append(Whight)
        elif current_floor >= 8:
            eligible.append(Phantasm)
            if random.random() < 0.25: eligible.append(Whight)
        elif current_floor >= 5:
            eligible.append(Lizardman)
            if random.random() < 0.25: eligible.append(Phantasm)
        elif current_floor >= 4:
            eligible.append(Lizardman)
        elif current_floor >= 2:
            eligible.append(Skeleton)
            if random.random() < 0.5: eligible.append(Zombie)
        elif current_floor >= 1:
            eligible.append(Zombie)
            
        if eligible:
            EnemyClass = random.choice(eligible)
            return EnemyClass(x, y)
        return None

    @staticmethod
    def spawn_construct(current_floor, x, y):
        if current_floor >= 4 and random.random() < 0.50:
            return Construct(x, y)
        return None

    @staticmethod
    def spawn_rats(current_floor, x, y):
        """Возвращает список крыс (от 1 до 2), либо пустой список."""
        rats = []
        if current_floor < 10 and random.random() < 0.6:
            RatClass = AngryRat if current_floor == 6 else Rat
            num_rats = random.randint(1, 2)
            for _ in range(num_rats):
                rats.append(RatClass(x, y))
        return rats

class ItemFactory:
    """Фабрика для создания лута."""

    @staticmethod
    def get_enemy_drop(enemy_char, x, y, game_mode='endless'):
        """Возвращает список предметов, выпадающих с врага."""
        if enemy_char in ('G', 'K', 'Q'):
            return [DungeonKey(x, y)]
        elif enemy_char == 'R': # RatKing
            return [DungeonKey(x, y)] + [RatMeat(x, y) for _ in range(5)]
        elif enemy_char == 'D': # DeathKnight
            return [DungeonKey(x, y), SoulReaper(x, y)]
        elif enemy_char == 'N': # Nightmare
            items = [WhiteMask(x, y)]
            if game_mode == 'endless': items.append(DungeonKey(x, y))
            return items
        elif enemy_char in ('r', 'a'): # Крысы и Злые крысы
            return [RatMeat(x, y)] if random.random() < 0.5 else []
        elif enemy_char == 'S':
            return [OldSword(x, y)]
        elif enemy_char == 'Z':
            return [CurvedSword(x, y)]
        elif enemy_char == 'C':
            return [LifeGem(x, y)]
        return []

    @staticmethod
    def generate_chest_loot(spawned_equipment_names):
        """Генерирует лут для сундука с учетом уже найденной экипировки."""
        loot = []
        spawned_names_this_chest = set()
        available_equipment = [HatOfKnowledge, Glasses, Chainmail, GlovesOfDexterity, Spear, Buckler, LeggingsOfStrength, AchillesSandals, CurvedSword]
        
        unseen_equipment = [eq for eq in available_equipment if eq.__name__ not in spawned_equipment_names]
        if not unseen_equipment: unseen_equipment = available_equipment
            
        eq_class = random.choice(unseen_equipment)
        loot.append(eq_class(0, 0))
        spawned_equipment_names.add(eq_class.__name__)
        spawned_names_this_chest.add(eq_class.__name__)
        
        loot.append(PotionOfHealing(0, 0))
        
        for _ in range(random.randint(0, 2)):
            if random.random() < 0.6:
                if random.random() < 0.5: loot.append(RatMeat(0, 0))
                else: loot.append(LifeGem(0, 0))
            else:
                possible_eq = [eq for eq in available_equipment if eq.__name__ not in spawned_names_this_chest]
                if not possible_eq:
                    loot.append(RatMeat(0, 0))
                    continue
                eq_class = random.choice(possible_eq)
                loot.append(eq_class(0, 0))
                spawned_equipment_names.add(eq_class.__name__)
                spawned_names_this_chest.add(eq_class.__name__)
                
        return loot
