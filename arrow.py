from config import ARROW_ANGLE, ARROW_SUB_ANGLE, ARROW_RECESS
import pygame as pg
import math

def get_vector(angle : float, size : float = 1):
    return pg.Vector2(math.cos(angle), math.sin(angle)) * size

def draw_arrow(surface : pg.Surface, origin : pg.Vector2, angle : float, length : float, color : pg.Color, size: int):
    end_pos = origin + pg.Vector2(math.cos(angle), math.sin(angle)) * length
    head_left = end_pos - get_vector(angle - ARROW_ANGLE, size)
    head_right = end_pos - get_vector(angle + ARROW_ANGLE, size)
    subsize = size * (1 - ARROW_RECESS)
    subpart_left = end_pos - get_vector(angle - ARROW_SUB_ANGLE, subsize)
    subpart_right = end_pos - get_vector(angle + ARROW_SUB_ANGLE, subsize)
    pg.draw.polygon(surface, color, [end_pos, head_left, subpart_left, origin, subpart_right, head_right])
