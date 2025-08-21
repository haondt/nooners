import curses
import time
import random
import copy

# y, x

BACKGROUND_SYMBOL = " "
ANT_SYMBOL = "@"
NUM_ANTS = 6  # 3 originally number of ants 
STEP_DELAY = 0.02  # faster for visibility

class Ant():
    def __init__(self, color_pair, height, width):
        self._dir = (0, 1)
        self.symbol = ANT_SYMBOL
        self._height = height
        self._width = width
        self._pos = (random.randint(0, height - 1), random.randint(0, width - 1))
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

    def step(self, grid, next_grid):
        y, x = self._pos
        is_white = (grid[y][x] == 0)

        # decide turn and flip state in next_grid
        if is_white:
            self._turn_right()
            next_grid[y][x] = 1  # flip to black
        else:
            self._turn_left()
            next_grid[y][x] = 0  # flip to white

        # walk
        new_y = y + self._dir[0]
        new_x = x + self._dir[1]
        # wrap
        new_y %= self._height
        new_x %= self._width
        self._pos = (new_y, new_x)


def _main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 255, -1)
    stdscr.bkgd(BACKGROUND_SYMBOL, curses.color_pair(1))

    height, width = stdscr.getmaxyx()
    width -= 1

    # initialize grid: 0 = white, 1 = black
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # init ants
    available_colors = [i for i in range(1, min(256, curses.COLORS))]
    random.shuffle(available_colors)
    ants = []
    for i in range(NUM_ANTS):
        color = available_colors.pop()
        pair_id = i + 2
        curses.init_pair(pair_id, color, -1)
        ants.append(Ant(pair_id, height, width))

    try:
        while True:
            # prepare next grid as copy of current
            next_grid = copy.deepcopy(grid)

            # randomize processing order
            order = list(ants)
            random.shuffle(order)

            # each ant reads grid and writes into next_grid
            for ant in order:
                ant.step(grid, next_grid)

            # commit
            grid = next_grid

            # redraw entire grid background
            for y in range(height):
                for x in range(width):
                    char = BACKGROUND_SYMBOL if grid[y][x] == 0 else ANT_SYMBOL
                    # draw black cells with default color
                    stdscr.addch(y, x, char, curses.color_pair(1))

            # draw ants on top
            for ant in ants:
                y, x = ant._pos
                stdscr.addch(y, x, ant.symbol, curses.color_pair(ant.color_pair))

            stdscr.refresh()
            if STEP_DELAY > 0:
                time.sleep(STEP_DELAY)
    except KeyboardInterrupt:
        pass


def main():
    curses.wrapper(_main)

if __name__ == '__main__':
    main()
