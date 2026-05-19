from actors.entity import Entity

class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, char="@", hp=10, base_attack=1, str_stat=1, dex_stat=1, con_stat=1)
        self.level = 1
        self.xp = 0
        self.stat_points = 0
        
        self.inventory = []
        self.equipment = {
            'head': None, 'face': None, 'chest': None, 'hands': None,
            'main_hand': None, 'off_hand': None, 'legs': None, 'feet': None
        }
        
        self.turns_waited = 0
        self.regen_clock = 0
        
        # Базовое здоровье (растет при level_up)
        self.base_max_hp = 10
        self._recalculate_max_hp()
        
        # Голод
        self.max_hunger = 300
        self.hunger = 300
        self._update_max_hunger()

    def _get_equip_stat_bonus(self, stat_name):
        """Суммирует бонусы к характеристикам от всей экипировки."""
        total = 0
        for item in self.equipment.values():
            if item and hasattr(item, 'stat_bonuses'):
                total += item.stat_bonuses.get(stat_name, 0)
        return total

    def get_total_str(self): return self.str_stat + self._get_equip_stat_bonus('str')
    def get_total_dex(self): return self.dex_stat + self._get_equip_stat_bonus('dex')
    def get_total_con(self): return self.con_stat + self._get_equip_stat_bonus('con')

    def _recalculate_max_hp(self):
        """Пересчитывает максимальное здоровье с учетом CON и экипировки."""
        con_bonus = (self.con_stat - 1) * 2
        equip_hp_bonus = sum(item.max_hp_bonus for item in self.equipment.values() if item and hasattr(item, 'max_hp_bonus'))
        
        new_max = self.base_max_hp + con_bonus + equip_hp_bonus
        
        if new_max > self.max_hp:
            diff = new_max - self.max_hp
            self.max_hp = new_max
            self.hp += diff # Экипировка лечит
        else:
            old_max = self.max_hp
            self.max_hp = new_max
            self.hp = min(self.hp, self.max_hp) # Снятие экипировки урезает текущее ХП

    def _update_max_hunger(self):
        new_max = 300 + ((self.con_stat - 1) * 30)
        if new_max > self.max_hunger:
            diff = new_max - self.max_hunger
            self.max_hunger = new_max
            self.hunger += diff
        else:
            self.max_hunger = new_max
            self.hunger = min(self.hunger, self.max_hunger)

    def get_hunger_status(self):
        pct = self.hunger / self.max_hunger
        if pct >= 0.75: return "Sated"
        elif pct >= 0.50: return "Peckish"
        elif pct >= 0.25: return "Hungry"
        else: return "Starving"

    def has_key(self):
        return any(item.name == "Dungeon Key" for item in self.inventory)

    def add_item(self, item):
        if item.category == 'equipment':
            # Собираем имена всего, что есть в рюкзаке и надето на игроке
            owned_names = [i.name for i in self.inventory]
            for eq in self.equipment.values():
                if eq is not None:
                    owned_names.append(eq.name)
            
            # Если имя предмета уже есть в списке - отказываем
            if item.name in owned_names:
                return False
                
            self.inventory.append(item)
            return True
            
        elif item.category == 'consumable':
            for inv_item in self.inventory:
                if inv_item.name == item.name:
                    if inv_item.quantity + item.quantity <= inv_item.max_stack:
                        inv_item.quantity += item.quantity
                        return True
                    else:
                        return False
            self.inventory.append(item)
            return True
            
        elif item.category == 'key':
            if not self.has_key():
                self.inventory.append(item)
                return True
            return False
            
        return False

    def remove_item(self, item, qty=1):
        if item in self.inventory:
            item.quantity -= qty
            if item.quantity <= 0:
                self.inventory.remove(item)

    def use_item(self, item):
        if item.name == "Rat Meat":
            hp_before = self.hp
            self.hp = min(self.max_hp, self.hp + 4)
            healed = self.hp - hp_before
            hunger_before = self.hunger
            self.hunger = min(self.max_hunger, self.hunger + item.nutrition_value)
            fed = self.hunger - hunger_before
            self.remove_item(item, 1)
            return f"You ate the Rat Meat! (+{healed} HP, +{fed} Hunger)"
        return "Cannot use this item."

    def equip_item(self, item):
        if item.slot and item.slot in self.equipment:
            # Логика двуручного оружия (Копье)
            if item.two_handed:
                if self.equipment['off_hand']:
                    self.inventory.append(self.equipment['off_hand'])
                    self.equipment['off_hand'] = None
            elif item.slot == 'off_hand' and self.equipment['main_hand'] and self.equipment['main_hand'].two_handed:
                self.inventory.append(self.equipment['main_hand'])
                self.equipment['main_hand'] = None

            current_equipped = self.equipment[item.slot]
            if current_equipped:
                self.inventory.append(current_equipped)
            
            self.inventory.remove(item)
            self.equipment[item.slot] = item
            
            # Если предмет двуручный, дублируем ссылку в off_hand
            if item.two_handed:
                self.equipment['off_hand'] = item
                
            self._recalculate_max_hp()
            return f"Equipped {item.name}."
        return "Cannot equip this."

    def unequip_item(self, slot_name):
        item = self.equipment[slot_name]
        if item:
            # Если предмет двуручный, очищаем оба слота
            if item.two_handed:
                if self.equipment['main_hand'] == item:
                    self.equipment['main_hand'] = None
                if self.equipment['off_hand'] == item:
                    self.equipment['off_hand'] = None
            else:
                self.equipment[slot_name] = None
                
            # Добавляем в инвентарь только один раз
            if item not in self.inventory:
                self.inventory.append(item)
                
            self._recalculate_max_hp()
            return f"Unequipped {item.name}."
        return "Nothing to unequip."

    def get_attack_damage(self):
        """Вычисляет урон с учетом экипировки."""
        total_bonus = sum(item.attack_bonus for item in self.equipment.values() if item)
        
        # Оружие увеличивает МИНИМАЛЬНЫЙ урон
        min_dmg = self.base_attack + total_bonus
        # Сила увеличивает МАКСИМАЛЬНЫЙ урон
        max_dmg = self.base_attack + self.get_total_str()
        
        # Бонус от 5 базовой Силы: +2 к минимальному урону
        if self.str_stat >= 5:
            min_dmg += 2
        
        # Штраф за голод
        if self.get_hunger_status() == "Starving":
            min_dmg = max(1, min_dmg - 1)
            max_dmg = max(1, max_dmg - 1)
            
        # Защита от багов
        if min_dmg > max_dmg:
            max_dmg = min_dmg
            
        import random
        return random.randint(min_dmg, max_dmg)

    def get_crit_chance(self):
        base_crit = 1 + (self.get_total_dex() * 3) # База от ЛОВКОСТИ
        equip_crit = sum(item.crit_bonus for item in self.equipment.values() if item and hasattr(item, 'crit_bonus'))
        return base_crit + equip_crit

    def take_damage(self, amount, is_crit=False):
        # 1. Блокировка Щитом
        block_chance = sum(item.block_chance for item in self.equipment.values() if item and hasattr(item, 'block_chance'))
        if block_chance > 0:
            import random
            if random.randint(1, 100) <= block_chance:
                if is_crit:
                    # Крит пробивает блок, но становится обычной атакой
                    return super().take_damage(amount // 2) # Половина урона (или можно вернуть amount без удвоения, если уже прошел double)
                else:
                    return 0 # Полный блок

        # 2. Снижение урона от CON и Кольчуги
        total_reduction = 0
        if self.con_stat >= 5: total_reduction += 1
        total_reduction += sum(item.dmg_reduction for item in self.equipment.values() if item and hasattr(item, 'dmg_reduction'))
        
        actual_damage = max(0, amount - total_reduction)
        self.hp -= actual_damage
        return actual_damage

    def gain_xp(self, amount):
        # Бонус опыта от Шляпы
        xp_bonus = sum(item.xp_bonus for item in self.equipment.values() if item and hasattr(item, 'xp_bonus'))
        self.xp += amount + xp_bonus
        if self.xp >= self.xp_to_next_level():
            self.level_up()

    def tick_hunger(self):
        if self.hunger > 0: self.hunger -= 1
        if self.hunger <= 0: self.hp -= 1

    def xp_to_next_level(self):
        if self.level == 1: return 5
        return 5 * (2 ** (self.level - 1))

    def level_up(self):
        self.xp -= self.xp_to_next_level()
        self.level += 1
        self.stat_points += 2
        
        # Увеличиваем базовое здоровье
        hp_gain = 4 + ((self.con_stat - 1) * 2)
        self.base_max_hp += hp_gain
        
        self._recalculate_max_hp()
        
        # Полное исцеление при повышении уровня
        self.hp = self.max_hp
        
        self._update_max_hunger()
        if self.xp >= self.xp_to_next_level():
            self.level_up()

    # Стоимость прокачки берется из БАЗОВЫХ статов
    def get_stat_cost(self, stat_name):
        base_val = getattr(self, f"{stat_name}_stat")
        if base_val == 4: return 3
        return 1

    def increase_stat(self, stat_name):
        cost = self.get_stat_cost(stat_name)
        if self.stat_points >= cost:
            if stat_name == 'str': self.str_stat += 1
            elif stat_name == 'dex': self.dex_stat += 1
            elif stat_name == 'con':
                self.con_stat += 1
                self._update_max_hunger()
                self._recalculate_max_hp()
            self.stat_points -= cost
            return True
        return False

    def reset_regen(self):
        self.turns_waited = 0
        self.regen_clock = 0

    def process_regen(self):
        if self.hunger <= 0:
            self.reset_regen()
            return
        if self.hp < self.max_hp:
            self.turns_waited += 1
            if self.turns_waited >= 10:
                self.regen_clock += 1
                if self.regen_clock >= 3:
                    self.hp = min(self.max_hp, self.hp + 1)
                    self.regen_clock = 0
        else:
            self.reset_regen()

    # UI Методы
    def get_attack_power(self):
        """Возвращает строку для UI вида '2-4' или '3'."""
        total_bonus = sum(item.attack_bonus for item in self.equipment.values() if item)
        
        min_dmg = self.base_attack + total_bonus
        max_dmg = self.base_attack + self.get_total_str()
        
        # Бонус от 5 базовой Силы
        if self.str_stat >= 5:
            min_dmg += 2
        
        if self.get_hunger_status() == "Starving":
            min_dmg = max(1, min_dmg - 1)
            max_dmg = max(1, max_dmg - 1)
            
        if min_dmg > max_dmg:
            max_dmg = min_dmg
            
        if min_dmg == max_dmg:
            return str(min_dmg)
        return f"{min_dmg}-{max_dmg}"

    def get_stat_description(self, stat_name):
        if stat_name == 'str': return "Increases maximum damage by 1 for each point. 5 base STR gives +2 minimum damage"
        elif stat_name == 'dex': return "Increases dodge chance by 5%, crit chance by 3% per point. 5 base DEX gives an extra turn"
        elif stat_name == 'con': return "Increases max HP gain per level by 2, max hunger by 30 per point. 5 base CON reduces damage by 1"
        return ""