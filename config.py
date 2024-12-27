from math import pi
from pygame import Color

def lerp(start, end, t):
    if t < 0: return start
    if t > 1: return end
    return int(start + (end - start) * t)

#SCREEN:
WIDTH = 1000
HEIGHT = 500

#ARROWS:
ARROW_ANGLE = pi / 6
ARROW_SUB_ANGLE = pi / 12
ARROW_RECESS = 0.2

#GISMOS:
GISMO_ARROW_HEAD_SIZE = 0.15
GISMO_COLOR = Color(255, 255, 255)
GISMO_CIRCLE_WIDTH = 1

#PATH:
PATH_LINE_WIDTH = 3
def get_path_color(x : int, y : int) -> Color:
    t = (x / WIDTH + y / HEIGHT) / 2
    return Color(lerp(255, 128, t), lerp(238, 0, t), lerp(118, 128, t))
