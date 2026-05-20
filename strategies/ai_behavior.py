import random
import abc

class AIBehavior(abc.ABC):
    @abc.abstractmethod
    def get_action(self, entity, game_map, player, enemies):
        pass

class PassiveAI(AIBehavior):
    def get_action(self, entity, game_map, player, enemies):
        directions = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]
        dx, dy = random.choice(directions)
        from actions.commands import MoveCommand
        return MoveCommand(entity, dx, dy, game_map, player, enemies)

class AggressiveAI(AIBehavior):
    def __init__(self):
        self.is_awake = False

class MediumAggressiveAI(AggressiveAI):
    def get_action(self, entity, game_map, player, enemies):
        if not self.is_awake:
            from actions.commands import WaitCommand
            return WaitCommand()

        dx_dist = abs(player.x - entity.x)
        dy_dist = abs(player.y - entity.y)
        distance = max(dx_dist, dy_dist)
        
        if distance <= 5:
            step_dx = 1 if player.x > entity.x else (-1 if player.x < entity.x else 0)
            step_dy = 1 if player.y > entity.y else (-1 if player.y < entity.y else 0)
            from actions.commands import MoveCommand
            return MoveCommand(entity, step_dx, step_dy, game_map, player, enemies)
        else:
            from actions.commands import WaitCommand
            return WaitCommand()
        
class ShortAggressiveAI(AggressiveAI):
    def get_action(self, entity, game_map, player, enemies):
        if not self.is_awake:
            from actions.commands import WaitCommand
            return WaitCommand()

        dx_dist = abs(player.x - entity.x)
        dy_dist = abs(player.y - entity.y)
        distance = max(dx_dist, dy_dist)
        
        if distance <= 3:
            step_dx = 1 if player.x > entity.x else (-1 if player.x < entity.x else 0)
            step_dy = 1 if player.y > entity.y else (-1 if player.y < entity.y else 0)
            from actions.commands import MoveCommand
            return MoveCommand(entity, step_dx, step_dy, game_map, player, enemies)
        else:
            from actions.commands import WaitCommand
            return WaitCommand()
