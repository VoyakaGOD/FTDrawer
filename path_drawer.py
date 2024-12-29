from config import CANVAS_WIDTH, CANVAS_HEIGHT, PATH_LINE_WIDTH
from config import get_path_color
import pygame as pg

BLACK = pg.Color(0, 0, 0)

class PathDrawer:
    def __init__(self, initial_point : pg.Vector2):
        self.previous_point = initial_point
        self.surface = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.surface.fill(BLACK)

    def add_point(self, point : tuple[int, int]):
        pg.draw.line(self.surface, get_path_color(point[0], point[1]), self.previous_point, point, PATH_LINE_WIDTH)
        self.previous_point = point

    def draw(self, canvas : pg.Surface):
        canvas.blit(self.surface, (0, 0))
