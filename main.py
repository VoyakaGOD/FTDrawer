from svg import get_coefficients
from gismos_system import GismosSystem
from path_drawer import PathDrawer
from config import WIDTH, HEIGHT
import pygame as pg

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FTDrawer")
clock = pg.time.Clock()
running = True

gismos_drawer = GismosSystem(pg.Vector2(400, 100), 100, get_coefficients("M 100 100 L 300 200", 5))
path_drawer = PathDrawer(gismos_drawer.get_point())

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    gismos_drawer.update(clock.get_time() / 1e6)
    path_drawer.add_point(gismos_drawer.get_point())
    path_drawer.draw(screen)
    gismos_drawer.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
