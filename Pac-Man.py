import pygame
import json
import sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pygame.init()

dis_width = 672
dis_height = 864

block = 32

name = 1

game_over = False

dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption("Poc-Man")


class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path, x1, y1):
        super().__init__() 
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [x1, y1]
        self.x, self.y = x1 * block, y1 * block
        self.vx, self.vy = 0, 0
        self.score = 0
        self.speed = 2

    def getPoints(self):
        if pygame.sprite.spritecollide(self, dot_group, True):
            self.score = max_score-len(dot_group)
        if pygame.sprite.spritecollide(pacman, enemy_group, False):
            sys.exit(0)

    def getKey(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed
        if keys[pygame.K_UP]:
            self.vy = -self.speed
        if keys[pygame.K_DOWN]:
            self.vy = self.speed

    def collideWithWalls(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, wall_group, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def otherSide(self):
        if self.x + self.vx < 0:
            self.x = dis_width - block
        if self.x + self.vx > dis_width:
            self.x = 0

    def update(self):
        self.getKey()
        self.otherSide()
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collideWithWalls('x')
        self.rect.y = self.y
        self.collideWithWalls('y')
        self.getPoints()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x * block
        self.rect.y = y * block
        self.speed = speed
        self.pos = self.rect.center
        self.direction = pygame.math.Vector2(0, 0)

        self.path = []
        self.collision_rect = []

    def get_coord(self):
        column = self.rect.centerx // 32
        rows = self.rect.centery // 32
        return column, rows

    def set_path(self, path):
        self.path = path
        self.create_collision_rect()
        self.get_direction()

    def create_collision_rect(self):
        if self.path:
            self.collision_rect = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                rect = pygame.Rect((x, y), (4, 4))
                self.collision_rect.append(rect)

    def get_direction(self):
        if self.collision_rect:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rect[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collisions(self):
        if self.collision_rect:
            for rect in self.collision_rect:
                if rect.collidepoint(self.pos):
                    del self.collision_rect[0]
                    self.get_direction()

    def update(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos


class Pathfinder:
    def __init__(self, mtx, player, en, name1):
        self.matrix = matrix
        self.grid = Grid(matrix=mtx)

        self.path = []

        self.enemy = en
        self.player = player
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)
        self.name = name1

    def create_path(self):
        start_x, start_y = self.enemy.get_coord()
        start = self.grid.node(start_x, start_y)

        end_x = self.player.rect.x // 32
        end_y = self.player.rect.y // 32
        if self.name == 1:
            if self.player.vx > 0:
                end_x += 2
            if self.player.vx < 0:
                end_x -= 2
            if self.player.vy > 0:
                end_y += 2
            if self.player.vy < 0:
                end_y -= 2
        elif self.name == 2:
            if self.player.vx > 0:
                end_x -= 1
            if self.player.vx < 0:
                end_x += 1
            if self.player.vy > 0:
                end_y -= 1
            if self.player.vy < 0:
                end_y += 1
        end = self.grid.node(end_x, end_y)

        finder = AStarFinder()
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.enemy.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                points.append((x, y))
            pygame.draw.lines(dis, '#4a4a4a', False, points, 5)

    def update(self):
        self.draw_path()
        self.enemy_group.update()
        self.enemy_group.draw(dis)
        if(self.path==""):
            self.create_path()


class Dot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # self.image = pygame.Surface((block, block))
        self.image = pygame.image.load('Dot.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x * block + block/2, pos_y * block + block/2)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("wall.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * block
        self.rect.y = pos_y * block


clock = pygame.time.Clock()
frame_rate = 60

pacman = Player("pacman.png", 10, 15)
enemies = [Enemy(10, 9, 2, "enemy.png"), Enemy(4, 9, 1.6, "enemy2.png"), Enemy(16, 9, 1.8, "enemy3.png")]

pacman_group = pygame.sprite.Group()
pacman_group.add(pacman)

with open('map1.json') as f:
    matrix = json.load(f)
matrix = json.loads(matrix)

pathfinder = []
enemy_group = pygame.sprite.Group()

for enemy in enemies:
    pathfinder.append(Pathfinder(matrix, pacman, enemy, name))
    enemy_group.add(enemy)
    name += 1

font = pygame.font.Font(None, 50)
score_surface = font.render(f'Score: {pacman.score}', False, 'White')
score_rect = score_surface.get_rect()
score_rect.center = (dis_width/2, 625)

with open('level1.json') as f:
    data = json.load(f)
data = json.loads(data)

dot_group = pygame.sprite.Group()
for col, row in data["dots"]:
    new_dot = Dot(col, row)
    dot_group.add(new_dot)

wall_group = pygame.sprite.Group()
for col, row in data["walls"]:
    new_wall = Wall(col, row)
    wall_group.add(new_wall)

level_setup = pygame.surface.Surface((dis_width, dis_height))
wall_group.draw(level_setup)

max_score = len(dot_group)

i = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_over = True

    i += 1
    if i == 50:
        for pf in pathfinder:
            pf.create_path()
        i = 0

    score_surface = font.render(f'Score: {pacman.score}/{max_score}', False, 'White')
    score_rect = score_surface.get_rect()
    score_rect.center = (dis_width / 2, 750)

    if pacman.score == max_score:
        game_over = True

    dis.fill("Black")
    dis.blit(level_setup, (0, 0))
    dis.blit(score_surface, score_rect)
    dot_group.draw(dis)
    pacman_group.draw(dis)
    pacman_group.update()
    for pf in pathfinder:
        pf.update()
    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
quit()
