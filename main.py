from svg import get_coefficients, get_first_path_description
from gismos_system import GismosSystem
from path_drawer import PathDrawer
from config import WIDTH, HEIGHT
from camera import Camera
import pygame as pg
from sys import argv

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FTDrawer")
clock = pg.time.Clock()
running = True

if len(argv) < 4:
    print("Usage `python main.py [filename] [n] [f1]`")
    exit(-1)

description = get_first_path_description(argv[1])
description.fit_in(Camera.get_screen_size())
bounding_rect = description.get_bounding_rect().move(Camera.get_canvas_center())
gismos_drawer = GismosSystem(Camera.get_canvas_center(), float(argv[3]), get_coefficients(description, int(argv[2])))
path_drawer = PathDrawer(gismos_drawer.get_point())
camera = Camera()

while running:
    # Events:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        else:
            camera.handle_event(event)
    # Update:
    delta_time = clock.get_time() / 1e3 # in seconds
    gismos_drawer.update(delta_time)
    path_drawer.add_point(gismos_drawer.get_point())
    camera.update(delta_time)
    # Draw:
    path_drawer.draw(camera.get_canvas())
    gismos_drawer.draw(camera.get_canvas())
    # todo: fix, pg.draw.rect(camera.get_canvas(), (255, 0, 0), bounding_rect, 3)
    camera.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
