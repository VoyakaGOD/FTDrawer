from config import WIDTH, HEIGHT, PATH_LINE_WIDTH
from config import get_path_color
import pygame as pg

BLACK = pg.Color(0, 0, 0)

class PathDrawer:
    def __init__(self, initial_point : pg.Vector2):
        self.previous_point = initial_point
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.surface.fill(BLACK)

    def add_point(self, point : tuple[int, int]):
        pg.draw.line(self.surface, get_path_color(point[0], point[1]), self.previous_point, point, PATH_LINE_WIDTH)
        self.previous_point = point

    def draw(self, surface : pg.Surface):
        surface.blit(self.surface, (0, 0))
