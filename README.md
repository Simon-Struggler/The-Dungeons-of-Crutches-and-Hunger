# The-Dungeons-of-Crutches-and-Hunger
This is my first attempt at creating a game using Python. I wanted to make a classic Roguelike, similar to Rogue 1980 or Moria 1983 - a procedurally generated turn-based dungeon crawler with RPG elements, permadeath and ASCII graphics.

--- LAUNCHING THE GAME ---

You're going to need the 'curses' package. Use the 'pip install windows-curses' command. Once done, launch the game by typing 'python main.py' or 'py main.py', whichever works for you.
Though you could always launch this game in github codespaces. I'm pretty sure you don't need to pip install curses that way.

--- CONTROLS ---
1. Movement. You can move laterally using the arrowkeys or WASD. For diagonal movement you can bind the keys you prefer in the settings menu (the section where you choose a gamemode), the default are "[" "]" ";" "'". Changed settings don't persist after quitting the game. Also, you can use the 'e' key to skip your turn. Holding it long enough will begin a meditation process which restores HP until disturbed, just watch out for hunger.
2. Attacking. You can attack enemies by simply walking into them. There is also an option to force-attack a tile, for which you must either press the 'f' key and then a direction in which to attack, or press ctrl+direction key - useful for weapons with long reach attacks (don't use ctrl+w in codespaces or it will close the tab, ctrl+s doesn't work).
3. Inventory. Press the 'i' key to open a multipurpose character menu. 
              The left section shows your stat-line. Pressing Enter on any stat will give you the option of either increasing it or reading information about the stat.
              The middle section is your character's equipment. It will show which equipment slots you have occupied.
              The right section is your inventory. There, you will find all the items you've picked up. Speaking of which...
4. Interacting with objects on the map. You can use the 'o' key in combination with a lateral direction key to open either a door ('+') or a chest ('c'). Use the 'g' key when standing on a tile with an item to pick it up.
5. Going to the next floor. Kill the 'G'oblin keymaster, pick up the 'k'ey, walk over a 'L'adder tile and press 'v' to descend.
6. Quitting the game. Press 'q' while the game map is open, then press 'Esc' to quit the game.
7. Praying. If you find yourself stuck for some reason (no key to go to a lower level, no Ladder to go down, etc.) press 'p' to pray. First prayer is the 'eye' to see beyond what mortals can. The second prayer is the 'key' so you can proceed below. The third prayer is the 'faz'e to step through solid wall to reach what can't be reached. The fourth and last prayer sends you straight 'dwn' to a level below, though beware - you are missing out of exp and loot to face the stronger foes.

I hope there won't be any crashes. Bugs are expected. Especially with the map generation. I've yet to figure out how to completely rule out the possibility of there being no descent ladder on the map. Certain mobs ('G' and 'S') can't chase the player if the player sees them in a room straight away (because some rooms lack a door leading to them from the starting room). Don't expect a bug report feature, though, you know how to contact me through normal means. Please do so.
