import pygame

class Mino:
    SHAPES = {
        "I": [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
        ],
        "O": [
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
        ],
        "T": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "S": [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "Z": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ],
        "J": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
        "L": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
    }

    COLORS = {
        "I": (80, 220, 220),
        "O": (240, 220, 70),
        "T": (170, 100, 230),
        "S": (90, 200, 110),
        "Z": (220, 90, 90),
        "J": (90, 120, 230),
        "L": (240, 160, 70),
    }

    def __init__(self, kind, spawn_x=3, spawn_y=-1):
        self.kind = kind
        self.rotation = 0
        self.x = spawn_x
        self.y = spawn_y
        self.color = self.COLORS[kind]

    def cells(self, offset_x=0, offset_y=0, rotation_delta=0):
        rotation = (self.rotation + rotation_delta) % 4
        return [(self.x + x + offset_x, self.y + y + offset_y) for x, y in self.SHAPES[self.kind][rotation]]

    def rotated_cells_right(self):
        return self.cells(rotation_delta=1)

    def rotated_cells_left(self):
        return self.cells(rotation_delta=-1)

    def rotate_right(self):
        self.rotation = (self.rotation + 1) % 4

    def rotate_left(self):
        self.rotation = (self.rotation - 1) % 4

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def draw(self, surface, cell_size, origin, border_color):
        ox, oy = origin
        for x, y in self.cells():
            if y < 0:
                continue
            rect = pygame.Rect(ox + x * cell_size, oy + y * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, border_color, rect, 1)