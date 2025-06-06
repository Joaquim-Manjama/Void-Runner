import pygame
import random as r

class Background:
    def __init__(self, image):
        self.image = image
        self.white_speed = 1
        self.medium_speed = 0.75
        self.dark_speed = 0.5
        self.white_stars = []
        self.medium_stars = []
        self.dark_stars = []
        self.white_colour = '#ffffff'
        self.medium_colour = '#3C4C68'
        self.dark_colour= '#1F2A3A'
        self.boost = False

    def reset(self):
        self.boost = False
        self.white_speed = 1
        self.medium_speed = 0.75
        self.dark_speed = 0.5

    def render(self, surf, offset=[0, 0]):
        surf.blit(self.image, (0 + offset[0], 0 + offset[1]))
        for star in self.white_stars:
            box = pygame.Rect(star[0] + offset[0], star[1] + offset[1], 2, 2)
            pygame.draw.rect(surf, self.white_colour, box)

        for star in self.medium_stars:
            box = pygame.Rect(star[0] + offset[0], star[1] + offset[1], 2, 2)
            pygame.draw.rect(surf, self.medium_colour, box)

        for star in self.dark_stars:
            box = pygame.Rect(star[0] + offset[0], star[1] + offset[1], 2, 2)
            pygame.draw.rect(surf, self.dark_colour, box)

    def update(self):
        if r.random() < 0.1:
            self.white_stars.append([650, r.randint(5, 430)])
        
        if r.random() < 0.1:
            self.medium_stars.append([650, r.randint(5, 430)])

        if r.random() < 0.1:
            self.dark_stars.append([650, r.randint(5, 430)])

        for star in self.white_stars.copy():
            star[0] -= self.white_speed if not self.boost else self.white_speed * 7
            if star[0] < -5:
                 self.white_stars.remove(star)

        for star in self.medium_stars.copy():
            star[0] -= self.medium_speed if not self.boost else self.medium_speed * 7
            if star[0] < -5:
                 self.medium_stars.remove(star)

        for star in self.dark_stars.copy():
            star[0] -= self.dark_speed if not self.boost else self.dark_speed * 7
            if star[0] < -5:
                 self.dark_stars.remove(star)

