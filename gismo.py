from config import GISMO_ARROW_HEAD_SIZE, GISMO_CIRCLE_WIDTH
from arrow import draw_arrow
import pygame as pg

def draw_gismo(surface : pg.Surface, origin : pg.Vector2, angle : float, radius : float, color : pg.Color):
    pg.draw.circle(surface, color, origin, radius, GISMO_CIRCLE_WIDTH)
    draw_arrow(surface, origin, angle, radius, color, GISMO_ARROW_HEAD_SIZE * radius)
