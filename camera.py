from config import WIDTH, HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT
from config import CAMERA_MOVEMENT_SPEED
from config import KeyBindings
import pygame as pg

class Camera:
    def __init__(self):
        self.canvas = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.restore()

    def get_screen_size():
        return pg.Vector2(WIDTH, HEIGHT)
    
    def get_screen_center():
        return Camera.get_screen_size() / 2

    def get_canvas_size():
        return pg.Vector2(CANVAS_WIDTH, CANVAS_HEIGHT)

    def get_canvas_center():
        return Camera.get_canvas_size() / 2

    def get_canvas(self):
        return self.canvas
    
    def restore(self):
        self.position = pg.Vector2(WIDTH - CANVAS_WIDTH, HEIGHT - CANVAS_HEIGHT) / 2
        self.scale = 1

    def draw(self, surface : pg.Surface):
        scaled = pg.transform.scale(self.canvas, Camera.get_canvas_size() * self.scale)
        surface.blit(scaled, self.position)

    def move(self, delta : pg.Vector2):
        self.position -= delta

    def change_scale(self, factor : float):
        self.position -= (Camera.get_screen_center() - self.position) * (factor - 1)
        self.scale *= factor

    def update(self, dt : float):
        keys = pg.key.get_pressed()
        if keys[KeyBindings.LEFT]: self.move(pg.Vector2(-CAMERA_MOVEMENT_SPEED, 0) * dt)
        if keys[KeyBindings.RIGHT]: self.move(pg.Vector2(CAMERA_MOVEMENT_SPEED, 0) * dt)
        if keys[KeyBindings.UP]: self.move(pg.Vector2(0, -CAMERA_MOVEMENT_SPEED) * dt)
        if keys[KeyBindings.DOWN]: self.move(pg.Vector2(0, CAMERA_MOVEMENT_SPEED) * dt)

    def handle_event(self, event : pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == KeyBindings.RESTORE:
                self.restore()
            elif event.key == KeyBindings.ZOOM_IN:
                self.change_scale(1.5)
            elif event.key == KeyBindings.ZOOM_OUT:
                self.change_scale(1 / 1.5)
