from svg import get_coefficients, get_first_path_description
from gismos_system import GismosSystem
from path_drawer import PathDrawer
from config import WIDTH, HEIGHT
from config import PATH_BRIGHT_PART
from camera import Camera
import pygame as pg
from sys import argv

def main():
    # Check args:
    if len(argv) < 4:
        print("Usage `python main.py [filename] [n] [f1]`")
        exit(-1)
    # Init pygame:
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("FTDrawer")
    clock = pg.time.Clock()
    # Init main objects:
    filename = argv[1]
    n = int(argv[2])
    f1 = float(argv[3])
    description = get_first_path_description(filename)
    description.fit_in(Camera.get_screen_size())
    gismos_drawer = GismosSystem(Camera.get_canvas_center(), f1, get_coefficients(description, n))
    path_drawer = PathDrawer(gismos_drawer.get_point(), PATH_BRIGHT_PART / f1)
    camera = Camera()
    # Main loop:
    running = True
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
        path_drawer.update_tail_time(delta_time)
        # Draw:
        path_drawer.draw(camera.get_canvas())
        gismos_drawer.draw(camera.get_canvas())
        camera.draw(screen)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
