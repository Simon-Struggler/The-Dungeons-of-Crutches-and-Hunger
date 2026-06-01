import curses
from menu import Menu
from engine import Engine

# Единый словарь привязок клавиш. Формат: 'id': ord('символ')
keybindings = {
    'move_n': ord('w'),
    'move_s': ord('s'),
    'move_w': ord('a'),
    'move_e': ord('d'),
    'move_nw': ord('['),
    'move_ne': ord(']'),
    'move_sw': ord(';'),
    'move_se': ord("'"),
    'wait': ord('e'),
    'get': ord('g'),
    'open': ord('o'),
    'inventory': ord('i'),
    'force_attack': ord('f'),
    'descend': ord('v'),
    'pray': ord('p'),
    'quit': ord('q')
}

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    menu = Menu(stdscr)
    settings = menu.main_menu(keybindings)
    
    if settings and settings.get("start"):
        engine = Engine(stdscr, settings, keybindings)
        result = engine.run()
        if result == "dead":
            main(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)