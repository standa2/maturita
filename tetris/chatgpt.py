import pygame
import random

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 128, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

class Tetris:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.x, self.y = 3, 0
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {'shape': shape, 'color': color}

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]

    def valid_position(self, shape, offset_x=0, offset_y=0):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = x + self.x + offset_x
                    board_y = y + self.y + offset_y
                    if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT or (board_y >= 0 and self.board[board_y][board_x]):
                        return False
        return True

    def freeze_piece(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.y + y][self.x + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.x, self.y = 3, 0
        if not self.valid_position(self.current_piece['shape']):
            print("Game Over!")

    def clear_lines(self):
        lines_to_clear = [i for i in range(BOARD_HEIGHT) if all(self.board[i])]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * BOARD_WIDTH)
        self.score += len(lines_to_clear)

    def drop_piece(self):
        if self.valid_position(self.current_piece['shape'], offset_y=1):
            self.y += 1
        else:
            self.freeze_piece()

    def move_piece(self, dx):
        if self.valid_position(self.current_piece['shape'], offset_x=dx):
            self.x += dx

    def update(self):
        self.drop_piece()

    def draw(self, screen):
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece['color'], ((self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 500  # milliseconds

    running = True
    while running:
        screen.fill(BLACK)
        game.draw(screen)
        pygame.display.flip()

        fall_time += clock.get_time()
        if fall_time > fall_speed:
            game.update()
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    game.drop_piece()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

    pygame.quit()

if __name__ == "__main__":
    main()
