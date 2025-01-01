import sys
import pygame
from pygame.locals import *

SCREEN_X = 900
SCREEN_Y = 750
GRID_SIZE = 30
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

# 色の定義
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# (x, y, width, height)
TETRIS_BOX = ((270,120), (300, 600))
HOLD_BOX = ((120,120), (120, 120))
NEXT_BOX = ((600,120), (120, 600))

class Tetris():
    def __init__(self):
        self.draw_background()
        pass
    
    def draw_background(self):
        SCREEN.fill(GRAY)
        pygame.draw.rect(SCREEN, WHITE, TETRIS_BOX)
        pygame.draw.rect(SCREEN, WHITE, HOLD_BOX)
        pygame.draw.rect(SCREEN, WHITE, NEXT_BOX)
        
        # タイトル"TETRIS"
        font = pygame.font.Font(None, 55)
        title = font.render("TETRIS", True, (0,0,0))
        SCREEN.blit(title, (350, 10)) 
        # Hold
        hold = font.render("Hold", True, (0,0,0))
        SCREEN.blit(hold, (120, 80)) 
        # Next
        next = font.render("Next", True, (0,0,0))
        SCREEN.blit(next, (600, 80)) 

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    tetris = Tetris()
    tetris.run()