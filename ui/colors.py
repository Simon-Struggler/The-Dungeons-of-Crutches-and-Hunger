import curses

# Стандартные 8 цветов: BLACK, Red, Green, Yellow, Blue, Magenta, Cyan, White

# Определяем наши цветовые пары (Текст, Фон)
# Фон COLOR_BLACK - стандартный черный терминала
COLOR_PAIR_DEFAULT = 0
COLOR_PAIR_RED = 1
COLOR_PAIR_GREEN = 2
COLOR_PAIR_BLUE = 3
COLOR_PAIR_YELLOW = 4
COLOR_PAIR_MAGENTA = 5
COLOR_PAIR_CYAN = 6
COLOR_PAIR_WHITE = 7

def init_colors():
    """Инициализация цветовых пар. Вызывается один раз при старте."""
    curses.start_color()
    curses.use_default_colors() # Позволяет использовать стандартный цвет фона терминала (-1)
    
    # init_pair(номер_пары, цвет_текста, цвет_фона)
    curses.init_pair(COLOR_PAIR_RED, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_PAIR_GREEN, curses.COLOR_GREEN, -1)
    curses.init_pair(COLOR_PAIR_BLUE, curses.COLOR_BLUE, -1)
    curses.init_pair(COLOR_PAIR_YELLOW, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_PAIR_MAGENTA, curses.COLOR_MAGENTA, -1)
    curses.init_pair(COLOR_PAIR_CYAN, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_PAIR_WHITE, curses.COLOR_WHITE, -1)
