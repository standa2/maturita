import pygame
import random

viktoor = pygame.math.Vector2

screen_w = 1280
cell_size = 32
start_x = 480
start_y = 96
collums = 10
rows = 20
ofset_x = 15
ofset_y = 3

offset = viktoor(collums // 2-1, 0)

sprite_group = pygame.sprite.Group()

tetrominos = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
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
        self.stop_x = 800
        self.stop_y = 736
        self.interval = 150
        self.thing = pygame.USEREVENT + 0
        
    def grid(self):
        for x in range(start_x, self.stop_x, cell_size):
            for y in range(start_y, self.stop_y, cell_size):
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
            Tetromino.move(self)
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


blocks = [Block(pos) for pos in tetrominos[shape]]


class Tetromino:
    def __init__(self):
        pass

    def move(self):
        move_d = movement['down']
        for block in blocks:
            block.pos += move_d

            


