import pygame
import random

viktoor = pygame.math.Vector2
sprite = pygame.sprite.Group()

block_size = 32
colums = 10
rows = 20
ofset_x = 15
ofset_y = 5
field_w = colums + ofset_x
field_h = rows + ofset_y / 2
offset = viktoor(colums // 2-1, 0)


tetrominos = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'J': [(0, 0), (0, -1), (1, 0), (2, 0)],
    'L': [(0, 0), (0, -1), (-1, 0), (-2, 0)],
    'S': [(0, 0), (1, 0), (0, 1), (-1, 1)],
    'Z': [(0, 0), (-1, 0), (0, 1), (1, 1)],
    'O': [(0, 0), (1, 0), (1, 1), (0, 1)],
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)]
}


movement = {
    'l': viktoor(-1,0),
    'r': viktoor(1,0),
    'd': viktoor(0,1),
}

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.start_x = 480
        self.start_y = 96
        self.stop_x = 800
        self.stop_y = 736
        self.speed = 500  
        self.tetromino = Tetromino()
        self.last_update = pygame.time.get_ticks()

    def landing(self):
        if self.tetromino.landing:
            self.tetromino = Tetromino()

    def control(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move(direction='l')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move(direction='r')

    def grid(self):
        for x in range(self.start_x, self.stop_x, block_size):
            for y in range(self.start_y, self.stop_y, block_size):
                square = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.screen, (10,10,10), square, 1)

    def update(self):
        time = pygame.time.get_ticks()
        if time - self.last_update > self.speed:
            self.tetromino.update()
            self.landing()
            self.last_update = time
        sprite.update()

    def draw(self):
        self.grid()
        sprite.draw(self.screen)



class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.pos = viktoor(pos) + offset + (ofset_x,ofset_y)
        super().__init__(sprite)
        self.image = pygame.Surface([block_size,block_size])
        self.image.fill("green")
        self.rect = self.image.get_rect()

    def rect_pos(self):
        self.rect.topleft = self.pos * block_size

    def update(self):
        self.rect_pos()

    def is_collide(self, pos):
        x = int(pos.x)
        y = int(pos.y)
        if ofset_y <= y < field_h:
            if ofset_x <= x < field_w:
                return False
        return True


class Tetromino:
    def __init__(self):
        self.shape = random.choice(list(tetrominos.keys()))
        self.blocks = [Block(pos) for pos in tetrominos[self.shape]]
        self.landing = False

    def is_collide(self, block_pos):
        return any(map(Block.is_collide, self.blocks, block_pos))

    def move(self, direction):
        move_dir = movement[direction]
        new_block_pos = [block.pos + move_dir for block in self.blocks]
        collide = self.is_collide(new_block_pos)

        if not collide:
            for block in self.blocks:
                block.pos += move_dir
        elif direction == 'd':
            self.landing = True

    def update(self):
        self.move(direction='d')



