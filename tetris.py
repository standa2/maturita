import pygame
import random

viktoor = pygame.math.Vector2

cell_size = 32

colums = 10
rows = 20
ofset_x = 15
ofset_y = 5

field_w = colums + ofset_x
field_h = rows + ofset_y / 2

offset = viktoor(colums // 2-1, 0)

sprite_group = pygame.sprite.Group()

tetrominos = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'J': [(0, 0), (0, -1), (1, 0), (2, 0)],
    'L': [(0, 0), (0, -1), (-1, 0), (-2, 0)],
    'S': [(0, 0), (1, 0), (0, 1), (-1, 1)],
    'Z': [(0, 0), (-1, 0), (0, 1), (1, 1)],
    'O': [(0, 0), (1, 0), (1, 1), (0, 1)],
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)]
}

shape = random.choice(list(tetrominos.keys()))

movement = {
    'left': viktoor(-1,0),
    'right': viktoor(1,0),
    'down': viktoor(0,1),
}

move_l = movement['left']
move_r = movement['right']


class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.start_x = 480
        self.start_y = 96
        self.stop_x = 800
        self.stop_y = 736
        self.interval = 150
        self.thing = pygame.USEREVENT + 0
        
    def grid(self):
        for x in range(self.start_x, self.stop_x, cell_size):
            for y in range(self.start_y, self.stop_y, cell_size):
                square = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.screen, "white", square, 1)

    def timer(self):
        pygame.time.set_timer(self.thing, self.interval)

    def control(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            for block in blocks:
                block.pos += move_l
        elif pressed_key == pygame.K_RIGHT:
            for block in blocks:
                block.pos += move_r

    def draw(self):
        self.grid()
        sprite_group.draw(self.screen)

    def update(self, trigger):
        if trigger:
            Tetromino.update()
        sprite_group.update()



class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.pos = viktoor(pos) + offset + (ofset_x,ofset_y)
        super().__init__(sprite_group)
        self.image = pygame.Surface([cell_size,cell_size])
        self.image.fill("green")
        self.rect = self.image.get_rect()

    def rect_pos(self):
        self.rect.topleft = self.pos * cell_size

    def update(self):
        self.rect_pos()

    def is_collide(self, pos):
        x = int(pos.x)
        y = int(pos.y)
        if ofset_y <= y < field_h:
            if ofset_x <= x < field_w:
                return False
        return True

blocks = [Block(pos) for pos in tetrominos[shape]]

class Tetromino:
    def __init__(self):
        pass

    def is_collide(block_pos):
        return any(map(Block.is_collide, blocks, block_pos))

    def move(direction):
        move_dir = movement[direction]
        block_pos = [block.pos + move_dir for block in blocks]
        collide = Tetromino.is_collide(block_pos)
        if not collide:
            for block in blocks:
                block.pos += move_dir

    def update():
        Tetromino.move(direction='down')

            


