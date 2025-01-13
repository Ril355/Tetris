import sys
import pygame
from pygame.locals import *

# 画面サイズの定義
SCREEN_X = 900
SCREEN_Y = 750
GRID_SIZE = 30
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

# 色の定義
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# 画面内の枠定義
# (x, y, width, height)
TETRIS_BOX = ((270,120), (300, 600))
HOLD_BOX = ((120,120), (120, 120))
NEXT_BOX = ((600,120), (120, 600))

class Tetris():
    def __init__(self):
        self.draw_background()
    
    # 背景描写関数
    def draw_background(self):
        # 背景をグレイで染める
        SCREEN.fill(GRAY)

        # メインBOX描写
        pygame.draw.rect(SCREEN, WHITE, TETRIS_BOX)

        # HoldBoxを描写
        pygame.draw.rect(SCREEN, WHITE, HOLD_BOX)

        # NextBoxを描写
        pygame.draw.rect(SCREEN, WHITE, NEXT_BOX)
        
        # タイトル"TETRIS"を描写
        font = pygame.font.Font(None, 55)
        title = font.render("TETRIS", True, (0,0,0))
        SCREEN.blit(title, (350, 10)) 

        # Holdテキスト描写
        hold = font.render("Hold", True, (0,0,0))
        SCREEN.blit(hold, (120, 80)) 

        # Nextテキスト描写
        next = font.render("Next", True, (0,0,0))
        SCREEN.blit(next, (600, 80)) 

        # 画面表示を更新
        pygame.display.update()

    # メインの実行関数
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # ESCでゲーム終了
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                    # SPACEでゲーム開始
                    elif event.key == K_SPACE:
                        pass
                        

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    tetris = Tetris()
    tetris.run()