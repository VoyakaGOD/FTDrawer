from svg import get_coefficients, get_first_path
from gismos_system import GismosSystem
from path_drawer import PathDrawer
from config import WIDTH, HEIGHT
import pygame as pg

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FTDrawer")
clock = pg.time.Clock()
running = True

gismos_drawer = GismosSystem(pg.Vector2(400, 100), 100, get_coefficients(get_first_path("example.svg"), 150))
path_drawer = PathDrawer(gismos_drawer.get_point())

from config import CANVAS_WIDTH, CANVAS_HEIGHT
canvas = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
shift = pg.Vector2(0, 0)
scale = 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            shift += pg.Vector2(25, 0)
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            shift -= pg.Vector2(25, 0)
        if event.type == pg.KEYDOWN and event.key == pg.K_w:
            shift += pg.Vector2(0, 25)
        if event.type == pg.KEYDOWN and event.key == pg.K_s:
            shift -= pg.Vector2(0, 25)
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            shift = pg.Vector2(0, 0)
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            scale *= 1.5
        if event.type == pg.KEYDOWN and event.key == pg.K_e:
            scale /= 1.5
    gismos_drawer.update(clock.get_time() / 1e6)
    path_drawer.add_point(gismos_drawer.get_point())
    path_drawer.draw(canvas)
    gismos_drawer.draw(canvas)
    screen.blit(pg.transform.scale(canvas, pg.Vector2(CANVAS_WIDTH, CANVAS_HEIGHT) * scale), shift)
    pg.display.flip()
    clock.tick(60)

pg.quit()
