import pygame 
import random as r

class Object_Behaviour:
    def __init__(self, image, type, probability, speed=[0, 0], wait=[0, 0], bouncing=False):
        self.image = image
        self.type = type
        self.probability = probability
        self.probability_backup = probability
        self.speed = list(speed)
        self.wait = list(wait)
        self.bouncing = bouncing
        self.objects = []
        self.velocity = [0, 0]
        self.bounce_force = 1
        self.bounce_timer = 0
        self.boost = False
        self.spawn = [320, 480]

    def reset(self):
        self.objects = []
        self.wait[0] = 0
        self.boost = False
        self.speed = [2, 0] if self.type != 'rock' else [3, 2]
        self.spawn = [320, 480]
        self.probability = self.probability_backup

    def add_object(self):
        x = 650 if self.type != 'rock' else r.randint(self.spawn[0], self.spawn[1])
        y = r.randint(0, 420) if self.type != 'rock' else -30
        self.objects.append([x, y])
        self.wait[0] = self.wait[1]

    def render(self, surf, offset=[0, 0]):
        for object in self.objects:
            surf.blit(self.image, (object[0] + offset[0], object[1] + offset[1]))

    def update(self):
        for object in self.objects:
            if self.bouncing:
                if self.bounce_timer % 5 == 0:
                    object[1] += self.velocity[1]
                    self.velocity[1] += self.bounce_force

                    if self.velocity[1] == 4 or self.velocity[1] == -4:
                        self.bounce_force *= -1

                self.bounce_timer += 1


            object[0] -= self.speed[0] if not self.boost else self.speed[0] * 7
            object[1] += self.speed[1] 
            if object[0] < -50 or object[1] >= 490:
                self.objects.remove(object)
                break

        if  r.random() < self.probability and self.wait[0] == 0:
            self.add_object()

        self.wait[0] = max(self.wait[0] - 1, 0)


    def display(self, surf):
        if self.type == 'magnet':
            pos = (500, 25)
        elif self.type == 'shift':
            pos = (20, 410)
        elif self.type == '2x':
            pos = (20, 80)
        elif self.type == 'booster':
            pos = (540, 405) 
        surf.blit(self.image, pos)
        


    def get_objects_rects(self):
        rects = []
        for object in self.objects:
            rects.append(pygame.Rect(object[0], object[1], self.image.get_width(), self.image.get_height()))
        return rects