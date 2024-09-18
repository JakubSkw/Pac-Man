import pygame
import json

pygame.init()

dis_height = 928
dis_width = 672
block = 32

dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption("Map generator")

background = pygame.Surface(dis.get_size())
c1, c2 = (32, 32, 32), (64, 64, 64)
tiles = [((x * block, y * block, block, block), c1 if (x + y) % 2 == 0 else c2) for x in range((dis_width + block) // block) for y in
         range((dis_height + block) // block)]
for rect, color in tiles:
    pygame.draw.rect(background, color, rect)

game_over = False

x1 = 400
y1 = 400


wall_list = []
dot_list = []

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                col = event.pos[0] // block
                row = event.pos[1] // block
                if not (col, row) in wall_list and not (col, row) in dot_list:
                    wall_list.append((col, row))
            elif event.button == 2:
                col = event.pos[0] // block
                row = event.pos[1] // block
                if not (col, row) in dot_list and not (col, row) in wall_list:
                    dot_list.append((col, row))
            elif event.button == 3:
                col = event.pos[0] // block
                row = event.pos[1] // block
                if (col, row) in wall_list:
                    wall_list.remove((col, row))
                if (col, row) in dot_list:
                    dot_list.remove((col, row))

    dis.blit(background, (0, 0))
    for col, row in wall_list:
        pygame.draw.rect(dis, "Blue", (col * block, row * block, block, block))
    for col, row in dot_list:
        pygame.draw.circle(dis, "White", [col * block + block/2, row * block + block/2], block/4)
    pygame.draw.circle(dis, "Yellow", [x1 - block / 2, y1 - block / 2], block / 2)

    pygame.display.update()

matrix=[]

for col in range(0, dis_width//block):
    l=[]
    for row in range(0, dis_height//block):
        if (row, col) in wall_list:
            l.append(0)
        else:
            l.append(1)
    matrix.append(l)

data_set = {"walls": wall_list, "dots": dot_list}
json_dump = json.dumps(data_set)

json_map = json.dumps(matrix)

with open('level.json', 'w') as f:
    json.dump(json_dump, f)

with open('map.json', 'w') as f:
    json.dump(json_map, f)

pygame.quit()
quit()