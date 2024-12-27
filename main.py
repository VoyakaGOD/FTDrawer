import pygame
import sys
from config import WIDTH, HEIGHT
from arrow import draw_arrow, get_vector

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FTDrawer")
clock = pygame.time.Clock()
running = True

angle = 0
angle2 = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    angle += clock.get_time() / 1e3
    angle2 += clock.get_time() / 5e2
    draw_arrow(screen, pygame.Vector2([200, 200]), angle, 100, (255, 255, 255))
    draw_arrow(screen, pygame.Vector2([200, 200]) + get_vector(angle, 100), angle2, 50, (205, 205, 205))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()