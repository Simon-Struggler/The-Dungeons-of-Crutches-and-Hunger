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

class MediumAggressiveAI(AIBehavior):
    def __init__(self):
        self.is_awake = False

    def get_action(self, entity, game_map, player, enemies):
        if not self.is_awake:
            from actions.commands import WaitCommand
            return WaitCommand()

        dx_dist = abs(player.x - entity.x)
        dy_dist = abs(player.y - entity.y)
        distance = max(dx_dist, dy_dist)
        
        if distance <= 5:
            step_dx = 0
            if player.x > entity.x: step_dx = 1
            elif player.x < entity.x: step_dx = -1
            
            step_dy = 0
            if player.y > entity.y: step_dy = 1
            elif player.y < entity.y: step_dy = -1
            
            from actions.commands import MoveCommand
            return MoveCommand(entity, step_dx, step_dy, game_map, player, enemies)
        else:
            from actions.commands import WaitCommand
            return WaitCommand()
        
class ShortAggressiveAI(AIBehavior):
    def __init__(self):
        self.is_awake = False

    def get_action(self, entity, game_map, player, enemies):
        if not self.is_awake:
            from actions.commands import WaitCommand
            return WaitCommand()

        dx_dist = abs(player.x - entity.x)
        dy_dist = abs(player.y - entity.y)
        distance = max(dx_dist, dy_dist)
        
        if distance <= 3:
            step_dx = 0
            if player.x > entity.x: step_dx = 1
            elif player.x < entity.x: step_dx = -1
            
            step_dy = 0
            if player.y > entity.y: step_dy = 1
            elif player.y < entity.y: step_dy = -1
            
            from actions.commands import MoveCommand
            return MoveCommand(entity, step_dx, step_dy, game_map, player, enemies)
        else:
            from actions.commands import WaitCommand
            return WaitCommand()
