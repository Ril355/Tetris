import pygame
import random

# テトリスのブロックの形状と色を定義
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]]
]
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (0, 255, 255)]

# ゲームの設定
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 2

# テトリスのクラス
class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_shape = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.new_block()

    def new_block(self):
        self.current_shape = random.choice(SHAPES)
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

    def check_collision(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if (
                    self.current_x + x < 0
                    or self.current_x + x >= GRID_WIDTH
                    or self.current_y + y >= GRID_HEIGHT
                    or (
                        self.current_y + y >= 0
                        and self.current_shape[y][x]
                        and self.grid[self.current_y + y][self.current_x + x]
                    )
                ):
                    return True
        return False

    def rotate(self):
        archive_shape = self.current_shape
        self.current_shape = [[self.current_shape[y][x] for y in range(len(self.current_shape))] for x in range(len(self.current_shape[0]) - 1, -1, -1)]
        if self.check_collision():
            self.current_shape = archive_shape

    def move_left(self):
        self.current_x -= 1
        if self.check_collision():
            self.current_x += 1

    def move_right(self):
        self.current_x += 1
        if self.check_collision():
            self.current_x -= 1

    def move_down(self):
        self.current_y += 1
        if self.check_collision():
            self.current_y -= 1
            self.merge_shape()
            self.clear_lines()
            self.new_block()
            if self.check_collision():
                self.game_over()

    def merge_shape(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if self.current_shape[y][x]:
                    self.grid[self.current_y + y][self.current_x + x] = self.current_shape[y][x]

    def clear_lines(self):
        full_lines = [index for index, row in enumerate(self.grid) if all(row)]
        for line_index in full_lines:
            del self.grid[line_index]
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 10

    def game_over(self):
        pygame.quit()
        quit()

    def draw(self, surface):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(surface, COLORS[self.grid[y][x]], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 5)
        if self.current_shape:
            for y in range(len(self.current_shape)):
                for x in range(len(self.current_shape[0])):
                    if self.current_shape[y][x]:
                        pygame.draw.rect(surface, COLORS[self.current_shape[y][x]], ((self.current_x + x) * GRID_SIZE, (self.current_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_UP:
                        self.rotate()

            self.move_down()

            surface.fill(COLORS[0])
            self.draw(surface)
            pygame.display.update()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Tetris()
    game.run()