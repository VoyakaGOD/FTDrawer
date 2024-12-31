from math import pi
import pygame as pg

def lerp(start, end, t):
    if t < 0: return start
    if t > 1: return end
    return int(start + (end - start) * t)

# SCREEN:
WIDTH = 1000
HEIGHT = 500

# CANVAS:
CANVAS_WIDTH = 2 * WIDTH
CANVAS_HEIGHT = 2 * HEIGHT

# ARROWS:
ARROW_ANGLE = pi / 6
ARROW_SUB_ANGLE = pi / 12
ARROW_RECESS = 0.2

# GISMOS:
GISMO_ARROW_HEAD_SIZE = 0.15
GISMO_COLOR = pg.Color(255, 255, 255)
GISMO_CIRCLE_WIDTH = 1
SHOW_CONSTANT_TERM = False

# PATH:
PATH_LINE_WIDTH = 3
def get_path_color(x : int, y : int) -> pg.Color:
    x = abs(x % 512 - 256)
    y = abs(y % 512 - 256)
    t = abs((x + y) / 256 - 1)
    return pg.Color(lerp(255, 128, t), lerp(238, 0, t), lerp(118, 128, t))

# INTERACTION:
CAMERA_MOVEMENT_SPEED = 350 # pixels per second
CAMERA_SHIFTED_MOVEMENT_SPEED = 750 # pixels per second
ZOOM_FACTOR = 1.5
MOUSE_WHEEL_ZOOM_FACTOR = 1.1
ZOOM_IN_LIMIT = 2.5
ZOOM_OUT_LIMIT = 2
class KeyBindings:
    UP = pg.K_w
    LEFT = pg.K_a
    DOWN = pg.K_s
    RIGHT = pg.K_d
    RESTORE = pg.K_f
    ZOOM_IN = pg.K_q
    ZOOM_OUT = pg.K_e
    SHIFT = pg.K_LSHIFT
