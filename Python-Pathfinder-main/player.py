import pygame, sys

class Player(object):

    def __init__(self, game):
        self.game = game

        self.x1 = self.game.dis_height/2
        self.y1 = self.game.dis_width/2

        self.x1_change = 0
        self.y1_change = 0
    def tick(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x1_change = -1
            self.y1_change = 0
        elif keys[pygame.K_RIGHT]:
            self.x1_change = 1
            self.y1_change = 0
        elif keys[pygame.K_UP]:
            self.y1_change = -1
            self.x1_change = 0
        elif keys[pygame.K_DOWN]:
            self.y1_change = 1
            self.x1_change = 0

        if self.x1+self.x1_change <= 0:
            self.x1 = self.game.dis_width
        elif self.x1+self.x1_change >= self.game.dis_width:
           self.x1 = self.game.block/2
        if self.y1+self.y1_change <= 0:
            self.y1 = self.game.dis_height
        elif self.y1+self.y1_change >= self.game.dis_height:
            self.y1 = self.game.block/2

        self.x1 += self.x1_change
        self.y1 += self.y1_change
    def draw(self):
        pygame.draw.circle(self.game.dis, (229, 255, 0), [self.x1, self.y1], self.game.block/2)