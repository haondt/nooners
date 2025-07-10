import curses
import time
import random

# y, x

BACKGROUND_SYMBOL = " "
ANT_SYMBOL = "@"
NUM_ANTS = 3
STEP_DELAY = 0.001

class Ant():
    def __init__(self, stdscr, color_pair):
        self._stdscr = stdscr
        self._dir = (0, 1)
        self.symbol = ANT_SYMBOL
        self._height, self._width = stdscr.getmaxyx()
        self._width -= 1 # idk why but it throws errors if i dont do this
        self._pos = (random.randint(0, self._height - 1), random.randint(0, self._width - 1))
        self.color_pair = color_pair

    def _turn_right(self):
        self._dir = {
            (1, 0): (0, 1),
            (0, 1): (-1, 0),
            (-1, 0): (0, -1),
            (0, -1): (1, 0),
        }[self._dir]

    def _turn_left(self):
        self._dir = {
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
            (0, 1): (1, 0),
        }[self._dir]

    def _walk(self):
        new_y = self._pos[0] + self._dir[0]
        new_x = self._pos[1] + self._dir[1]
        if new_y >= self._height:
            new_y = 0
        elif new_y < 0:
            new_y = self._height - 1;
        if new_x >= self._width:
            new_x = 0
        elif new_x < 0:
            new_x = self._width - 1;

        self._pos = (new_y, new_x)

    def step(self):
        is_white = chr(self._stdscr.inch(self._pos[0], self._pos[1]) & 0xFF) == BACKGROUND_SYMBOL

        if is_white:
            self._turn_right()
            self._stdscr.addch(self._pos[0], self._pos[1], self.symbol, curses.color_pair(self.color_pair))
        else:
            self._turn_left()
            self._stdscr.addch(self._pos[0], self._pos[1], BACKGROUND_SYMBOL)
        self._walk()


def _main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 255, -1)
    stdscr.bkgd(BACKGROUND_SYMBOL, curses.color_pair(1))

    available_colors = [i for i in range(1, min(256, curses.COLORS))]
    random.shuffle(available_colors)

    ants = []
    for i in range(NUM_ANTS):
        color = available_colors.pop()
        pair_id = i + 2
        curses.init_pair(pair_id, color, -1)
        ants.append(Ant(stdscr, pair_id))

    try:
        while True:
            for ant in ants:
                ant.step()
            stdscr.refresh()
            if STEP_DELAY > 0:
                time.sleep(STEP_DELAY)
    except:
        raise Exception(f"{ant._pos}, {ant._dir}, {ant._width}, {ant._height}")


def main():
    curses.wrapper(_main)

if __name__ == '__main__':
    main()
