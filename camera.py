from config import WIDTH, HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT
from config import CAMERA_MOVEMENT_SPEED, CAMERA_SHIFTED_MOVEMENT_SPEED
from config import ZOOM_IN_LIMIT, ZOOM_OUT_LIMIT, ZOOM_FACTOR, MOUSE_WHEEL_ZOOM_FACTOR
from config import KeyBindings
import pygame as pg

class Camera:
    def __init__(self):
        self.canvas = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.restore()
        self.mouse_position = None
        self.is_dragged = False

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
        scaled = pg.transform.scale_by(self.canvas, self.scale)
        surface.blit(scaled, self.position)

    def move(self, delta : pg.Vector2):
        self.position -= delta
        self.position = pg.Vector2(min(self.position.x, 0), 
                                   min(self.position.y, 0))
        self.position = pg.Vector2(max(self.position.x, WIDTH - CANVAS_WIDTH * self.scale), 
                                   max(self.position.y, HEIGHT - CANVAS_HEIGHT * self.scale))

    def change_scale(self, factor : float):
        if self.scale * factor > ZOOM_IN_LIMIT: return
        if self.scale * factor < (1 / ZOOM_OUT_LIMIT): return
        self.position -= (Camera.get_screen_center() - self.position) * (factor - 1)
        self.scale *= factor
        self.move(pg.Vector2(0, 0))

    def update(self, dt : float):
        keys = pg.key.get_pressed()
        delta = CAMERA_MOVEMENT_SPEED
        if keys[KeyBindings.SHIFT]:
            delta = CAMERA_SHIFTED_MOVEMENT_SPEED
        delta *= dt
        if keys[KeyBindings.LEFT]: self.move(pg.Vector2(-delta, 0))
        if keys[KeyBindings.RIGHT]: self.move(pg.Vector2(delta, 0))
        if keys[KeyBindings.UP]: self.move(pg.Vector2(0, -delta))
        if keys[KeyBindings.DOWN]: self.move(pg.Vector2(0, delta))

    def handle_event(self, event : pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == KeyBindings.RESTORE:
                self.restore()
            elif event.key == KeyBindings.ZOOM_IN:
                self.change_scale(ZOOM_FACTOR)
            elif event.key == KeyBindings.ZOOM_OUT:
                self.change_scale(1 / ZOOM_FACTOR)
        elif event.type == pg.MOUSEWHEEL:
            self.change_scale(MOUSE_WHEEL_ZOOM_FACTOR ** event.y)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.mouse_position = pg.mouse.get_pos()
            self.is_dragged = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_dragged = False
        elif (event.type == pg.MOUSEMOTION) and self.is_dragged:
            new_mouse_position = pg.Vector2(*pg.mouse.get_pos())
            self.move(self.mouse_position - new_mouse_position)
            self.mouse_position = new_mouse_position
