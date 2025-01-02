from config import CANVAS_WIDTH, CANVAS_HEIGHT, PATH_LINE_WIDTH
from config import PATH_QUEUE_LIMIT, PATH_DARKENING_FACTOR
from config import get_path_color
import pygame as pg

BLACK = pg.Color(0, 0, 0)

def darken(color : pg.Color):
    return pg.Color(int(color.r * PATH_DARKENING_FACTOR), int(color.g * PATH_DARKENING_FACTOR), int(color.b * PATH_DARKENING_FACTOR))

class PathDrawer:
    def __init__(self, initial_point : pg.Vector2, tail_allowance_time : float):
        self.previous_point = initial_point
        self.surface = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.surface.fill(BLACK)
        self.queue = []
        self.tail_time_left = tail_allowance_time

    def remove_tail(self):
        if len(self.queue) == 0:
            raise Exception("No tail!")
        tail_start, tail_end = self.queue.pop(0)
        pg.draw.line(self.surface, darken(get_path_color(tail_end[0], tail_end[1])), tail_start, tail_end, PATH_LINE_WIDTH)

    def update_tail_time(self, dt : float):
        if self.tail_time_left > -1:
            self.tail_time_left -= dt

    def add_point(self, point : tuple[int, int]):
        pg.draw.line(self.surface, get_path_color(point[0], point[1]), self.previous_point, point, PATH_LINE_WIDTH)
        if PATH_QUEUE_LIMIT > 0:
            self.queue += [(self.previous_point, point)]
            if (len(self.queue) > PATH_QUEUE_LIMIT) or (self.tail_time_left < 0):
                self.remove_tail()
        self.previous_point = point

    def draw(self, canvas : pg.Surface):
        canvas.blit(self.surface, (0, 0))
