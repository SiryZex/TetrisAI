from settings import *
import pygame.freetype as ft
import math

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 3.5, bgcolor=(45, 45, 45))
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),
                            text='NEXT', fgcolor='orange',
                            size=TILE_SIZE * 3.5, bgcolor=(45, 45, 45))
        self.font.render_to(self.app.screen, (WIN_W * 0.61, WIN_H * 0.67),
                            text='SCORE', fgcolor='orange',
                            size=TILE_SIZE * 3.5, bgcolor=(45, 45, 45))
        self.font.render_to(self.app.screen, (WIN_W * 0.61, WIN_H * 0.8),
                            text=f'{self.app.score}', fgcolor='white',
                            size=TILE_SIZE * 3, bgcolor=(45, 45, 45))
        
    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
				(255,255,255), (0,0,0))
		
        msgim_center_x, msgim_center_y = msg_image.get_size()
        msgim_center_x //= 2
        msgim_center_y //= 2
		
        self.screen.blit(msg_image, (
            self.width // 2-msgim_center_x,
            self.height // 2-msgim_center_y+i*22))