import pygame
import random as r

class Laser:
    def __init__(self):
        self.width = 640
        self.height = 1
        self.lasers = [[0, 130], [0, 260], [0, 390]]
        self.timer = 0
        self.probability = 0.00125

    def reset(self):
        self.timer = 0
        self.probability = 0.00125

    def render(self, surf):
        if self.timer > 1800:
            if self.timer > 1860:
                colour = '#d95763'
            else:
                colour = '#ff0000'
            for laser in self.lasers:
                pygame.draw.rect(surf, colour, self.get_rect(laser))

    def update(self):  
        self.timer = max(self.timer -  1, 0)
        if self.timer == 0:
            if r.random() < self.probability:
                self.timer = 2040
    

    def get_rect(self, list=[0, 0]):
        return pygame.Rect(list[0], list[1], self.width, self.height)

    def get_rects(self):
        rects = []
        for laser in self.lasers:
            rects.append(self.get_rect(laser))

        return rects

    


    