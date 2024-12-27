from gismo import draw_gismo
from arrow import get_vector
import pygame as pg
from math import pi

class GismosSystem():
    def __init__(self, origin : pg.Vector2, carrier_frequency : float, coefficients : list[float]):
        self.origin = origin
        self.gismos = []
        for n, c in enumerate(coefficients):
            if c == 0: continue
            self.gismos += [[c, 2 * pi * carrier_frequency * n, 0]] # coefficient, frequency, angle

    def update(self, dt : float):
        for gismo in self.gismos:
            gismo[2] += gismo[1] * dt

    def draw(self, surface : pg.Surface):
        origin = self.origin.copy()
        for gismo in self.gismos:
            draw_gismo(surface, origin, gismo[2], gismo[0], (255, 255, 255))
            origin += get_vector(gismo[2], gismo[0])
