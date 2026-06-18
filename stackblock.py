import pygame

class StackBlock:
    def __init__(self, cols, rows, cell_size, origin):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.origin = origin
        self.grid = []
        self.reset()

    def reset(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def inside(self, x, y):
        return 0 <= x < self.cols and y < self.rows

    def collides(self, cells):
        for x, y in cells:
            if x < 0 or x >= self.cols or y >= self.rows:
                return True
            if y >= 0 and self.grid[y][x] is not None:
                return True
        return False

    def lock(self, cells, color):
        for x, y in cells:
            if 0 <= y < self.rows:
                self.grid[y][x] = color

    def clear_lines(self):
        kept = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.rows - len(kept)
        for _ in range(cleared):
            kept.insert(0, [None for _ in range(self.cols)])
        self.grid = kept
        return cleared

    def draw(self, surface, border_color=(0, 0, 0)):
        ox, oy = self.origin
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    ox + x * self.cell_size,
                    oy + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                if cell is not None:
                    pygame.draw.rect(surface, cell, rect)
                pygame.draw.rect(surface, border_color, rect, 1)