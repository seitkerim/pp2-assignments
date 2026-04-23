import pygame
from ball import Ball

pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Game")

white = (255, 255, 255)
clock = pygame.time.Clock()

ball = Ball(width // 2, height // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:  # One press = one move
            ball.move(event.key, width, height)

    screen.fill(white)
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()