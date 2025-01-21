import pygame, random, pathlib
from utility import get_image
viktoor = pygame.math.Vector2

cell_size = 32
colums = 10
rows = 20

ofset_x = 15
ofset_y = 3
next_pos_ofset_x = 33
next_pos_ofset_y = 5

width = colums + ofset_x
height = rows + ofset_y 
center = viktoor(colums // 2, 0)
next_pos_ofset = viktoor(next_pos_ofset_x, next_pos_ofset_y)

tetrominos = {
    'T': [(0, 0), (0, 1), (-1, 0), (1, 0)],
    'J': [(0, 0), (-1, 0), (1, 0), (1, 1)],
    'L': [(0, 0), (-1, 0), (1, 0), (-1, 1)],
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

        self.level = 1
        self.kachow = 10
        self.normal = 600
        self.speed = self.normal

        self.L_points = 0
        self.J_points = 0
        self.S_points = 0
        self.Z_points = 0
        self.O_points = 0
        self.T_points = 0
        self.I_points = 0
        
        self.lines_destroyed = 0
        self.points = 0
        self.full_lines = 0
        self.points_per_line = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

        self.sprite = pygame.sprite.Group()
        self.field = self.array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.last_update1 = pygame.time.get_ticks()
        self.last_update2 = pygame.time.get_ticks()

    def score(self):
        self.points += self.points_per_line[self.full_lines] * self.level
        self.full_lines = 0

        if self.lines_destroyed < 10:
            self.level = 1
        if self.lines_destroyed >= 10 and self.lines_destroyed < 20:
            self.level = 2
        if self.lines_destroyed >= 20 and self.lines_destroyed < 30:
            self.level = 3
        if self.lines_destroyed >= 30 and self.lines_destroyed < 40:
            self.level = 4
        if self.lines_destroyed >= 40 and self.lines_destroyed < 50:
            self.level = 5
        if self.lines_destroyed >= 50 and self.lines_destroyed < 60:
            self.level = 6
        if self.lines_destroyed >= 60 and self.lines_destroyed < 70:
            self.level = 7
        if self.lines_destroyed >= 70 and self.lines_destroyed < 80:
            self.level = 8
        if self.lines_destroyed >= 80 and self.lines_destroyed < 90:
            self.level = 9
        if self.lines_destroyed >= 90:
            self.level = 10

        if self.level == 1:
            self.normal = 600
        if self.level == 2:
            self.normal = 500
        if self.level == 3:
            self.normal = 450
        if self.level == 4:
            self.normal = 400
        if self.level == 5:
            self.normal = 350
        if self.level == 6:
            self.normal = 300
        if self.level == 7:
            self.normal = 250
        if self.level == 8:
            self.normal = 200
        if self.level == 9:
            self.normal = 150
        if self.level == 10:
            self.normal = 100
        
    def lines(self):
        row = height - 1
        for y in range(height - 1, - 1, -1):
            for x in range(width):
                self.field[row][x] = self.field[y][x]
                if self.field[y][x]:
                    self.field[row][x].pos = viktoor(x,y)
            if sum(map(bool, self.field[y])) < colums:
                row -= 1
            else:
                for x in range(width):
                    self.sprite.remove(self.field[row][x])
                    self.field[row][x] = 0
                self.full_lines += 1
                self.lines_destroyed += 1

    def in_array(self):
        for cell in self.tetromino.cells:
            x = int(cell.pos.x)
            y = int(cell.pos.y)
            self.field[y][x] = cell

    def array(self):
        return [[0 for x in range(width)]for y in range(height)]
    
    def game_over(self):
        if self.tetromino.cells[0].pos.y == ofset_y:
            pygame.time.wait(1000)
            return True

    def new_tetromino(self):
        if self.tetromino.landed:
            if self.game_over():
                self.__init__(self.screen)
            else:
                self.in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
                self.speed = self.normal

    def control(self, key):
        down = pygame.key.get_pressed()
        if key == pygame.K_LEFT:
            self.tetromino.move(dir='l')
        if key == pygame.K_RIGHT:
            self.tetromino.move(dir='r')
        if key == pygame.K_UP:
            self.tetromino.rotate()
        if down[pygame.K_DOWN]:
            self.tetromino.move(dir='d')

    def grid(self):
        for x in range(self.start_x, self.stop_x, cell_size):
            for y in range(self.start_y, self.stop_y, cell_size):
                square = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.screen, (10,10,10), square, 1)

    def update(self):
        current_time1 = pygame.time.get_ticks()
        current_time2 = pygame.time.get_ticks()
        if current_time2 - self.last_update2 > self.kachow:
            self.lines()
            self.score()
            self.last_update2 = current_time2
        if current_time1 - self.last_update1 > self.normal:
            self.tetromino.update()
            self.new_tetromino()
            self.last_update1 = current_time1
        self.sprite.update()
        
    def draw(self):
        self.grid()
        self.sprite.draw(self.screen)

class Cell(pygame.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = viktoor(pos) + center + (ofset_x,ofset_y)
        self.next_pos = viktoor(pos) + next_pos_ofset
        self.live = True
        super().__init__(tetromino.tetris.sprite)

        if self.tetromino.tetris.level == 1:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_0/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 2:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_1/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 3:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_2/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 4:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_3/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 5:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_4/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 6:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_5/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 7:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_6/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 8:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_7/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 9:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_8/2.png").convert_alpha()
        elif self.tetromino.tetris.level == 10:
            if self.tetromino.shape == 'L':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/3.png").convert_alpha()
            elif self.tetromino.shape == 'Z':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/3.png").convert_alpha()
            elif self.tetromino.shape == 'S':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/1.png").convert_alpha()
            elif self.tetromino.shape == 'J':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/1.png").convert_alpha()
            elif self.tetromino.shape == 'T':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/2.png").convert_alpha()
            elif self.tetromino.shape == 'I':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/2.png").convert_alpha()
            elif self.tetromino.shape == 'O':
                self.spritesheet = pygame.image.load("assets/Blocks/lvl_9/2.png").convert_alpha()

        self.image = get_image(self.spritesheet, 0, 0, 48, 48, 0.7)
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.live:
            self.kill()

    def rotate(self, pivot):
        new_pos = self.pos - pivot
        rotated = new_pos.rotate(90)
        return rotated + pivot

    def rect_cell(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * cell_size

    def collided(self, pos):
        cell_x = int(pos.x)
        cell_y = int(pos.y)
        if ofset_x <= cell_x < width:
            if cell_y < height:
                if cell_y < ofset_y or not self.tetromino.tetris.field[cell_y][cell_x]:
                    return False
        return True
    
    def update(self):
        self.is_alive()
        self.rect_cell()

class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(tetrominos.keys()))
        self.cells = [Cell(self, pos) for pos in tetrominos[self.shape]]
        self.landed = False
        self.current = current

        if not self.current :
            if self.shape == 'L' :
                tetris.L_points += 1
            if self.shape == 'J' :
                tetris.J_points += 1
            if self.shape == 'S' :
                tetris.S_points += 1
            if self.shape == 'Z' :
                tetris.Z_points += 1
            if self.shape == 'O' :
                tetris.O_points += 1
            if self.shape == 'T' :
                tetris.T_points += 1
            if self.shape == 'I' :
                tetris.I_points += 1

    def rotate(self):
        pivot = self.cells[0].pos
        new_pos = [cell.rotate(pivot) for cell in self.cells]

        if not self.collided(new_pos) and self.shape != 'O':
            for i, cell in enumerate(self.cells):
                cell.pos = new_pos[i]

    def collided(self, cell_pos):
        return any(map(Cell.collided, self.cells, cell_pos))

    def move(self, dir):
        move_dir = movement[dir]
        current_cell_pos = [cell.pos + move_dir for cell in self.cells]
        collided = self.collided(current_cell_pos)

        if not collided:
            for cell in self.cells:
                cell.pos += move_dir
        elif dir == 'd':
            self.landed = True

    def update(self):
        self.move(dir='d')