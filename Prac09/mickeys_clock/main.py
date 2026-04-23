import pygame
import os
from clock import MickeyClock

pygame.init()

width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mickey's Clock")

clock = pygame.time.Clock()
mickey = MickeyClock(width, height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()   