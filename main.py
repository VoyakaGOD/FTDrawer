from gismos_system import GismosSystem
from config import WIDTH, HEIGHT
import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FTDrawer")
clock = pg.time.Clock()
running = True

drawer = GismosSystem(pg.Vector2(WIDTH / 2, HEIGHT / 2), 100, [0, 100, 75, 0, 20, 10, 5])

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    drawer.update(clock.get_time() / 1e6)
    screen.fill((0, 0, 0))
    drawer.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()