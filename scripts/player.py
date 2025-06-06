import pygame

class Player:
    def __init__(self, image, pos=[100, 100]):
        self.image = image
        self.pos = list(pos)
        self.jumping = False
        self.velocity = [0, 0]
        self.gravity = 1
        self.glow_time = 0
        self.glow_colour = None
        self.magnet = 0

    def reset(self):
        self.pos = [80, 180]
        self.velocity = [0, 0] 
        self.jumping = False
        self.gravity = 1
        self.magnet = 0

    def render(self, surf, offset=[0, 0]):
        if self.glow_time > 0:
            glow_rect = pygame.Rect(self.pos[0] - 2, self.pos[1] - 2, self.image.get_width() + 4, self.image.get_height() + 4)
            pygame.draw.rect(surf, self.glow_colour, glow_rect)
            pygame.draw.rect(surf, '#0a0e1a', self.get_rect())
            
        surf.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def update(self):
        self.pos[1] += self.velocity[1]
        self.pos[1] = max(self.pos[1], 0)

        if self.jumping:
            self.velocity[1] -= self.gravity
        else:
            self.velocity[1] += self.gravity

        self.velocity[1] = max(self.velocity[1], -4)
        self.velocity[1] = min(self.velocity[1], 4)  

        self.glow_time = max(self.glow_time - 1, 0)
        self.magnet = max(self.magnet - 1, 0)
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
    
    def glow(self, colour, time=30):
        if self.glow_time == 0:
            self.glow_time = time
            self.glow_colour = colour


    def has_collided(self, objects):
        i = 0
        player_rect = self.get_rect()
        for obj in objects:
            if player_rect.colliderect(obj):
                return [True, i]
            i += 1
        return [False, -1]
    
    def has_collided_magnet(self, objects):
        i = 0
        player_rect = pygame.Rect(self.pos[0], self.pos[1] - 300, self.image.get_width(), self.image.get_height() + 600)
        for obj in objects:
            if player_rect.colliderect(obj):
                return [True, i]
            i += 1
        return [False, -1]