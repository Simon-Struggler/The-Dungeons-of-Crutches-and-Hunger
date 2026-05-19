import curses
import os
import platform
from menu import Menu
from engine import Engine

# Глобальные настройки управления
keybindings = {
    'move_nw': None, # Северо-Запад
    'move_ne': None, # Северо-Восток
    'move_sw': None, # Юго-Запад
    'move_se': None  # Юго-Восток
}

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    menu = Menu(stdscr)
    # Передаем keybindings в меню, чтобы мы могли их менять
    settings = menu.main_menu(keybindings)
    
    if settings and settings.get("start"):
        # Передаем keybindings в движок
        engine = Engine(stdscr, settings, keybindings)
        result = engine.run()
        if result == "dead":
            main(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)