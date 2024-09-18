import pygame, sys
from player import Player

class Game(object):

    def __init__(self):
        self.frame_rate = 200.0
        self.block = 25

        pygame.init()
        self.dis_height = 700
        self.dis_width = 825

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        self.clock = pygame.time.Clock()

        self.player = Player(self)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.tick()   
            self.clock.tick(self.frame_rate)

            self.dis.fill((0, 0, 0))
            self.draw()
            pygame.display.update()

    def tick(self):
        self.player.tick()
    def draw(self):
        self.player.draw()

#x1 = dis_height/2
#y1 = dis_width/2

#x1_change = 0
#y1_change = 0
if __name__ == "__main__":
    Game()
