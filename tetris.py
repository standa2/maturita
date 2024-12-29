import pygame
import random

viktoor = pygame.math.Vector2
sprite = pygame.sprite.Group()

cell_size = 32
colums = 10
rows = 20
ofset_x = 15
ofset_y = 3
width = colums + ofset_x
height = rows + ofset_y 
center = viktoor(colums // 2-1, 0)

tetrominos = {
    'T': [(0, 0), (0, 1), (-1, 1), (1, 1)],
    'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
    'L': [(0, 0), (0, 1), (-1, 1), (-2, 1)],
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

    def new_tetromino(self):
        if self.tetromino.landed:
            self.tetromino = Tetromino()

    def control(self, key):
        if key == pygame.K_LEFT:
            self.tetromino.move(dir='l')
        elif key == pygame.K_RIGHT:
            self.tetromino.move(dir='r')

    def grid(self):
        for x in range(self.start_x, self.stop_x, cell_size):
            for y in range(self.start_y, self.stop_y, cell_size):
                square = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.screen, (10,10,10), square, 1)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.speed:
            self.tetromino.update()
            self.new_tetromino()
            self.last_update = current_time
        sprite.update()

    def draw(self):
        self.grid()
        sprite.draw(self.screen)

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.pos = viktoor(pos) + center + (ofset_x,ofset_y)
        super().__init__(sprite)
        self.image = pygame.Surface([cell_size,cell_size])
        self.image.fill("green")
        self.rect = self.image.get_rect()

    def rect_cell(self):
        self.rect.topleft = self.pos * cell_size

    def update(self):
        self.rect_cell()

    def collided(self, pos):
        cell_x = int(pos.x)
        cell_y = int(pos.y)
        if ofset_y <= cell_y < height:
            if ofset_x <= cell_x < width:
                return False
        return True

class Tetromino:
    def __init__(self):
        self.shape = random.choice(list(tetrominos.keys()))
        self.cells = [Block(pos) for pos in tetrominos[self.shape]]
        self.landed = False

    def collided(self, block_pos):
        return any(map(Block.collided, self.cells, block_pos))

    def move(self, dir):
        move_dir = movement[dir]
        current_block_pos = [block.pos + move_dir for block in self.cells]
        collided = self.collided(current_block_pos)

        if not collided:
            for block in self.cells:
                block.pos += move_dir
        elif dir == 'd':
            self.landed = True

    def update(self):
        self.move(dir='d')