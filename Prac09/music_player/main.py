import pygame
import os
from player import MusicPlayer

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

playlist = [
    (os.path.join(BASE_DIR, "music/Ed Sheeran -Shape of You.mp3"), os.path.join(BASE_DIR, "music/Shape of you.jpg")),
    (os.path.join(BASE_DIR, "music/The_Neighbourhood-Sweater_Weather.mp3"), os.path.join(BASE_DIR, "music/Sweather Weaher.jpg")),
    (os.path.join(BASE_DIR, "music/OneRepublic-Counting_Stars.mp3"), os.path.join(BASE_DIR, "music/Counting Stars.jpg")),
]

player = MusicPlayer(playlist)
player.play()

current_image = pygame.image.load(player.get_current_image())
current_image = pygame.transform.scale(current_image, (250, 250))

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

running = True
while running:
    screen.fill(WHITE)
    screen.blit(current_image, (175, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
                current_image = pygame.image.load(player.get_current_image())
                current_image = pygame.transform.scale(current_image, (250, 250))
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
                current_image = pygame.image.load(player.get_current_image())
                current_image = pygame.transform.scale(current_image, (250, 250))
            elif event.key == pygame.K_b:
                player.prev_track()
                current_image = pygame.image.load(player.get_current_image())
                current_image = pygame.transform.scale(current_image, (250, 250))
            elif event.key == pygame.K_q:
                running = False

    track_name = player.get_current_track().split("/")[-1]
    track_text = font.render(f"Now: {track_name}", True, BLACK)
    screen.blit(track_text, (50, 290))

    status = "Playing ▶" if player.is_playing else "Stopped ■"
    status_text = font.render(status, True, BLACK)
    screen.blit(status_text, (50, 330))

    controls = small_font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, GRAY)
    screen.blit(controls, (50, 370))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()