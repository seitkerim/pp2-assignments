import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, w, h):
        self.center = (w // 2, h // 2)

        base = os.path.dirname(__file__)
        img = os.path.join(base, "images")

        self.bg = pygame.image.load(os.path.join(img, "clock.png"))
        self.bg = pygame.transform.scale(self.bg, (w, h))

        self.body = pygame.image.load(os.path.join(img, "mickey.png")).convert_alpha()
        self.body = pygame.transform.scale(self.body, (350, 450))
        self.body_rect = self.body.get_rect(center=self.center)

        self.min_hand = pygame.image.load(os.path.join(img, "right_hand.png")).convert_alpha()
        self.min_hand = pygame.transform.scale(self.min_hand, (150, 200))

        self.sec_hand = pygame.image.load(os.path.join(img, "left_hand.png")).convert_alpha()
        self.sec_hand = pygame.transform.scale(self.sec_hand, (140, 200))

    def rotate(self, surf, img, pos, pivot, angle):
        rect = img.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset = pygame.math.Vector2(pos) - rect.center
        offset = offset.rotate(-angle)
        center = (pos[0] - offset.x, pos[1] - offset.y)

        rot_img = pygame.transform.rotate(img, angle)
        rot_rect = rot_img.get_rect(center=center)

        surf.blit(rot_img, rot_rect)

    def draw(self, screen):
        now = datetime.datetime.now()

        sec_angle = -now.second * 6
        min_angle = -now.minute * 6

        min_pivot = (self.min_hand.get_width() // 2, self.min_hand.get_height())
        sec_pivot = (self.sec_hand.get_width() // 2, self.sec_hand.get_height())

        screen.blit(self.bg, (0, 0))
        screen.blit(self.body, self.body_rect)

        self.rotate(screen, self.min_hand, self.center, min_pivot, min_angle)
        self.rotate(screen, self.sec_hand, self.center, sec_pivot, sec_angle)