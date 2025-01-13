import random

class Mino():
    # 座標
    SHAPES = [
        [[1, 1, 1, 1]],             # I字
        [[1, 1], [1, 1]],           # O字
        [[1, 0, 0], [1, 1, 1]],     # J字
        [[0, 0, 1], [1, 1, 1]],     # L字 
        [[1, 1, 0], [0, 1, 1]],     # Z字
        [[0, 1, 1], [1, 1, 0]],     # S字
        [[1, 1, 1], [0, 1, 0]]      # T字
    ]
    COLORS = [
        # (Red, Green, Blue)
        (0, 0, 0), 
        (255, 0, 0), 
        (0, 255, 0), 
        (0, 0, 255), 
        (255, 255, 0), 
        (255, 165, 0), 
        (0, 255, 255)
    ]

    def __init__(self, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE):
        # インスタンス生成時に各定数を取得
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.GRID_SIZE = GRID_SIZE
        # 初期化
        self.grid = [[0] * self.GRID_WIDTH for _ in range(self.GRID_HEIGHT)]
        self.current_shape = None
        self.current_x = 0
        self.current_y = 0
        pass

    def new_block(self):
        self.current_shape = random.choice(self.SHAPES)
        # テトリミノが生成される場所を指定（x軸は中央、y軸は一番上）
        self.current_x = self.GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

    def check_collision(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if (
                    self.current_x + x < 0
                    or self.current_x + x >= self.GRID_WIDTH
                    or self.current_y + y >= self.GRID_HEIGHT
                    or (
                        self.current_y + y >= 0
                        and self.current_shape[y][x]
                        and self.grid[self.current_y + y][self.current_x + x]
                    )
                ):
                    return True
        return False

    def move_down(self):
        # 1個下に落ちる
        self.current_y += 1
        # 衝突検知
        if self.check_collision():
            # めり込んだから戻す
            self.current_y -= 1
            self.merge_shape()
            # self.clear_lines()
            self.new_block()
            # if self.check_collision():
            #     self.game_over()

    def merge_shape(self):
        for y in range(len(self.current_shape)):
            for x in range(len(self.current_shape[0])):
                if self.current_shape[y][x]:
                    self.grid[self.current_y + y][self.current_x + x] = self.current_shape[y][x]

    def draw(self, surface):
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                pygame.draw.rect(surface, self.COLORS[self.grid[y][x]], (x * self.GRID_SIZE, y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 0)
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.GRID_WIDTH * self.GRID_SIZE, self.GRID_HEIGHT * self.GRID_SIZE), 5)
        if self.current_shape:
            for y in range(len(self.current_shape)):
                for x in range(len(self.current_shape[0])):
                    if self.current_shape[y][x]:
                        pygame.draw.rect(surface, self.COLORS[self.current_shape[y][x]], ((self.current_x + x) * self.GRID_SIZE, (self.current_y + y) * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE), 0)

    def rotate_right():
        pass

    def rotate_left():
        pass

    def move_right():
        pass

    def move_left():
        pass

    def draw_mino():
        pass