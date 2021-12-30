import time
import os
import math

import curses
from curses import wrapper
from _curses import error as curses_error

from graphics import *


class App:
    gradient = ' .:!/r(l1Z4H9W8$@'

    def __init__(self):
        self.is_running = True
        self.stdscr: curses.window = None
        terminal_size = os.get_terminal_size()
        self.screen_width = terminal_size.columns - 1
        self.screen_heigth = terminal_size.lines
        self.screen_aspect = self.screen_width / self.screen_heigth
        self.symbol_aspect = 9 / 19

        self.test_i = 0

    def handle_key(self, key):
        if key == 'q':
            self.is_running = False

    def draw_at(self, x, y, ch):
        if 0 <= x <= self.screen_width - 1 and 0 <= y <= self.screen_heigth - 1:
            self.stdscr.addstr(y, x, ch)

    def draw(self):
        self.test_i += 1
        light = Vec3(math.sin(self.test_i*0.1), math.cos(self.test_i*0.1), -1).norm()
        for i in range(self.screen_width):
            for j in range(self.screen_heigth):
                uv = Vec2(i, j) / Vec2(self.screen_width, self.screen_heigth) * 2 - 1
                uv.x *= self.screen_aspect * self.symbol_aspect
                ro = Vec3(-2, 0, 0)
                rd = Vec3(1, uv.x, uv.y).norm()
                ch = ' '
                color = 0

                intersection = sphere_intersection(ro, rd, 1)
                if intersection.x > 0:
                    it_point = ro + rd * intersection.x
                    n = it_point.norm()
                    diff = n.dot(light)
                    color = int(diff * 20)

                color = clamp(color, 0, len(self.gradient)-1)
                ch = self.gradient[color]
                self.draw_at(i, j, ch)

    def run(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)

        while self.is_running:
            try:
                key = stdscr.getkey()
            except curses_error:
                key = None
            self.handle_key(key)
            self.stdscr.clear()  # erase
            self.draw()
            self.stdscr.refresh()
            time.sleep(0.016)


if __name__ == '__main__':
    app = App()
    wrapper(app.run)
