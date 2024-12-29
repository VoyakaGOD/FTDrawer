from config import GISMO_COLOR
from gismo import draw_gismo
from arrow import get_vector
import pygame as pg
from math import pi
from cmath import phase

class GismosSystem:
    def __init__(self, origin : pg.Vector2, carrier_frequency : float, coefficients : list[complex]):
        self.origin = origin
        if len(coefficients) % 2 == 0:
            raise Exception("Coefficients array should be [c_{-n}, ..., c_{0}, ..., c_{n}]")
        n = len(coefficients) // 2
        self.gismos = []
        self.add_gismo(abs(coefficients[n]), 0, phase(coefficients[n]))
        for i in range(1, n + 1):
            c = coefficients[n - i]
            if c != 0: self.add_gismo(abs(c), 2 * pi * carrier_frequency * i, phase(c))
            c = coefficients[n + i]
            if c != 0: self.add_gismo(abs(c), -2 * pi * carrier_frequency * i, phase(c))

    def add_gismo(self, radius : float, omega : float, angle : float):
        self.gismos += [[radius, omega, angle]]

    def update(self, dt : float):
        for gismo in self.gismos:
            gismo[2] += gismo[1] * dt

    def draw(self, surface : pg.Surface):
        origin = self.origin.copy()
        for gismo in self.gismos:
            draw_gismo(surface, origin, gismo[2], gismo[0], GISMO_COLOR)
            origin += get_vector(gismo[2], gismo[0])

    def get_point(self):
        point = self.origin.copy()
        for gismo in self.gismos:
            point += get_vector(gismo[2], gismo[0])
        return int(point.x), int(point.y)
