import pygame as pg

class Button:
	#белые коробки - спрайты по умолчанию
    pg.init()
    whitebox_0 = pg.Surface((200, 200))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 0), (199, 0))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 0), (199, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 199), (0, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 199), (0, 0))
    whitebox_1 = whitebox_0.copy()
    pg.draw.line(whitebox_1, (200, 200, 200), (0, 0), (199, 199))
    pg.draw.line(whitebox_1, (200, 200, 200), (199, 0), (0, 199))
    
    def __init__ (self, x, y, w, h, sprite_0 = whitebox_0, sprite_1 = whitebox_1, state = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sprite_0 = sprite_0
        self.sprite_1 = sprite_1
        self.state = state
    
    def click (self, x_click, y_click):
    	#меняет состояние при попадании по кнопке
        if (self.x < x_click) & (self.x + self.w > x_click) & (self.y < y_click) & (self.y + self.h > y_click):
            self.state = not self.state
    
    def draw_butt (self, surface):
    	#в зависимости от состояния рисует нужный спрайт
        if self.state:
            if (self.w, self.h) != self.sprite_1.get_size():
                self.sprite_1 = pg.transform.smoothscale(self.sprite_1, (self.w, self.h))
            surface.blit(self.sprite_1, (self.x, self.y))
        else:
            if (self.w, self.h) != self.sprite_0.get_size():
                self.sprite_0 = pg.transform.smoothscale(self.sprite_0, (self.w, self.h)) 
            surface.blit(self.sprite_0, (self.x, self.y))

