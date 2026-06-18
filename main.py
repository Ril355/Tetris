import random
import sys
from collections import deque

import pygame
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_r, K_SPACE, K_UP, K_x, K_z, KEYDOWN, QUIT

from mino import Mino
from stackblock import StackBlock

SCREEN_X = 900
SCREEN_Y = 750
GRID_SIZE = 30

# 色の定義
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# (x, y), (width, height)
TETRIS_BOX = ((270, 120), (300, 600))
HOLD_BOX = ((120, 120), (120, 120))
NEXT_BOX = ((600, 120), (120, 600))


class Tetris:
    def hoge():
        pass
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = StackBlock(cols=10, rows=20, cell_size=GRID_SIZE, origin=TETRIS_BOX[0])
        self.drop_interval_ms = 500
        self.last_drop_at = pygame.time.get_ticks()
        self.game_over = False
        self.bag = []
        self.next_queue = deque()
        self.current = None
        self.reset_game()

    def reset_game(self):
        self.board.reset()
        self.bag = []
        self.next_queue = deque()
        while len(self.next_queue) < 3:
            self.next_queue.append(self.next_kind())
        self.game_over = False
        self.last_drop_at = pygame.time.get_ticks()
        self.spawn_next_piece()

    def next_kind(self):
        if not self.bag:
            self.bag = list(Mino.SHAPES.keys())
            random.shuffle(self.bag)
        return self.bag.pop()

    def spawn_next_piece(self):
        if len(self.next_queue) < 3:
            while len(self.next_queue) < 3:
                self.next_queue.append(self.next_kind())
        self.current = Mino(self.next_queue.popleft(), spawn_x=3, spawn_y=-1)
        self.next_queue.append(self.next_kind())
        if self.board.collides(self.current.cells()):
            self.game_over = True

    def try_move(self, dx, dy):
        candidate = self.current.cells(offset_x=dx, offset_y=dy)
        if self.board.collides(candidate):
            return False
        self.current.x += dx
        self.current.y += dy
        return True

    def try_rotate(self, clockwise=True):
        if clockwise:
            rotated = self.current.rotated_cells_right()
        else:
            rotated = self.current.rotated_cells_left()

        for kick_x in (0, -1, 1, -2, 2):
            kicked = [(x + kick_x, y) for x, y in rotated]
            if not self.board.collides(kicked):
                if clockwise:
                    self.current.rotate_right()
                else:
                    self.current.rotate_left()
                self.current.x += kick_x
                return True
        return False

    def hard_drop(self):
        while self.try_move(0, 1):
            pass
        self.lock_current_piece()

    def lock_current_piece(self):
        self.board.lock(self.current.cells(), self.current.color)
        self.board.clear_lines()
        self.spawn_next_piece()

    def update(self):
        if self.game_over:
            return
        now = pygame.time.get_ticks()
        if now - self.last_drop_at >= self.drop_interval_ms:
            self.last_drop_at = now
            if not self.try_move(0, 1):
                self.lock_current_piece()

    def handle_keydown(self, key):
        if key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if self.game_over:
            if key == K_r:
                self.reset_game()
            return

        if key == K_LEFT:
            self.try_move(-1, 0)
        elif key == K_RIGHT:
            self.try_move(1, 0)
        elif key == K_DOWN:
            if not self.try_move(0, 1):
                self.lock_current_piece()
        elif key in (K_UP, K_x):
            self.try_rotate(clockwise=True)
        elif key == K_z:
            self.try_rotate(clockwise=False)
        elif key == K_SPACE:
            self.hard_drop()

    def draw_static_ui(self):
        self.screen.fill(GRAY)
        pygame.draw.rect(self.screen, WHITE, (*TETRIS_BOX[0], *TETRIS_BOX[1]))
        pygame.draw.rect(self.screen, WHITE, (*HOLD_BOX[0], *HOLD_BOX[1]))
        pygame.draw.rect(self.screen, WHITE, (*NEXT_BOX[0], *NEXT_BOX[1]))

        title_font = pygame.font.Font(None, 55)
        ui_font = pygame.font.Font(None, 32)
        self.screen.blit(title_font.render("TETRIS", True, BLACK), (350, 10))
        self.screen.blit(title_font.render("Next", True, BLACK), (600, 80))
        self.screen.blit(ui_font.render("Controls", True, BLACK), (128, 130))
        self.screen.blit(ui_font.render("Move: <- ->", True, BLACK), (123, 165))
        self.screen.blit(ui_font.render("Rotate: Up / Z", True, BLACK), (123, 195))
        self.screen.blit(ui_font.render("Drop: Down / Space", True, BLACK), (123, 225))

    def draw_current_piece(self):
        if self.current is None or self.game_over:
            return
        self.current.draw(
            surface=self.screen,
            cell_size=GRID_SIZE,
            origin=TETRIS_BOX[0],
            border_color=BLACK,
        )

    def draw_next_preview(self):
        preview_size = 20
        preview_origin_x, preview_origin_y = NEXT_BOX[0]
        gap = 120
        label_font = pygame.font.Font(None, 32)
        self.screen.blit(label_font.render("Next+1", True, BLACK), (preview_origin_x + 12, preview_origin_y + 8))
        self.screen.blit(label_font.render("Next+2", True, BLACK), (preview_origin_x + 12, preview_origin_y + 8 + gap))

        for idx, kind in enumerate(list(self.next_queue)[:2]):
            mino = Mino(kind, spawn_x=0, spawn_y=0)
            blocks = Mino.SHAPES[kind][0]
            min_x = min(x for x, _ in blocks)
            max_x = max(x for x, _ in blocks)
            min_y = min(y for _, y in blocks)
            max_y = max(y for _, y in blocks)
            width = (max_x - min_x + 1) * preview_size
            height = (max_y - min_y + 1) * preview_size
            panel_y = preview_origin_y + 45 + idx * gap
            panel_x = preview_origin_x + (NEXT_BOX[1][0] - width) // 2
            panel_y += (70 - height) // 2
            for x, y in blocks:
                px = panel_x + (x - min_x) * preview_size
                py = panel_y + (y - min_y) * preview_size
                rect = pygame.Rect(px, py, preview_size, preview_size)
                pygame.draw.rect(self.screen, mino.color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw(self):
        self.draw_static_ui()
        self.board.draw(self.screen, border_color=BLACK)
        self.draw_current_piece()
        self.draw_next_preview()

        if self.game_over:
            overlay = pygame.Surface((TETRIS_BOX[1][0], TETRIS_BOX[1][1]), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, TETRIS_BOX[0])
            font = pygame.font.Font(None, 55)
            small = pygame.font.Font(None, 38)
            self.screen.blit(font.render("GAME OVER", True, WHITE), (305, 350))
            self.screen.blit(small.render("Press R to Restart", True, WHITE), (315, 400))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    self.handle_keydown(event.key)
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    tetris = Tetris(screen)
    tetris.run()