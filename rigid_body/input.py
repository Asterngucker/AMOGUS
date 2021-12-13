import pygame as pg
from math import *

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
        if (self.x < x_click) and (self.x + self.w > x_click) and (self.y < y_click) and (self.y + self.h > y_click):
            self.state = not self.state
    
    def draw (self, surface):
    	#в зависимости от состояния рисует нужный спрайт
        if self.state:
            if (self.w, self.h) != self.sprite_1.get_size():
                self.sprite_1 = pg.transform.smoothscale(self.sprite_1, (self.w, self.h))
            surface.blit(self.sprite_1, (self.x, self.y))
        else:
            if (self.w, self.h) != self.sprite_0.get_size():
                self.sprite_0 = pg.transform.smoothscale(self.sprite_0, (self.w, self.h)) 
            surface.blit(self.sprite_0, (self.x, self.y))


class Slider:
    '''
    крутилка, на которую можно нажать ЛКМ и потянуть мышкой.
    Вертикальная или горизонтальная, произвольный прямоугольник экранных осей.
    В slider.offset пишет смещение за кадр. 0 если не нажата.
    slider.offset_tot - суммирующееся смещение.
    '''
    def __init__(slider, pos, size, axis, offset_tot = 0):
        '''
        **pos**  — положение верхнего левого угла
        **size** — размер
        **axis** — ось: 0==x, 1==y
        '''
        slider.pos         = pos
        slider.size        = size
        slider.sprite      = None
        slider.pressed     = False
        slider.offset      = 0
        slider.offset_tot  = offset_tot
        slider.axis        = axis
        
        slider.upd_sprite()  
    
    def click (slider, pos):
        if slider.pos[0] < pos[0] and slider.pos[0]+slider.size[0] > pos[0] and slider.pos[1] < pos[1] and slider.pos[1]+slider.size[1] > pos[1]:
            slider.pressed = True
    
    def drag (slider, rel):
        if slider.pressed:
            slider.offset     += rel[slider.axis]
            slider.offset_tot += rel[slider.axis]
            slider.upd_sprite()
    
    def release (slider):
        if slider.pressed:
            slider.pressed = False
    
    @staticmethod
    def event_handler (sliders, events): # обработчик событий для крутилок. В список sliders стоит добавить все активные крутилки.
        for slider in sliders:
            slider.offset = 0
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for slider in sliders:
                    slider.click(event.pos)
            elif event.type == pg.MOUSEMOTION:
                for slider in sliders:
                    slider.drag(event.rel)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for slider in sliders:
                    slider.release()
    
    def upd_sprite (slider): 
        if slider.axis == 1:
            size = (slider.size[1], slider.size[0])
        else:
            size = slider.size
        sprite = pg.Surface(size)
        sprite.set_colorkey("0x000000")
        r = size[0]*0.5                                      #радиус колёсика. Отрисовывается вид с ребра.
        alph_interval = 0.15                                 #расстояние между рисками в радианах
        delta_dash = slider.offset_tot/(r*alph_interval)
        alph_offset = (delta_dash - round(delta_dash-0.5)) * alph_interval
        alph_0 = asin(size[0]/(2*r))
        alph = -alph_0 + alph_offset
        while alph < alph_0:
            line_x = size[0]/2 + r*sin(alph)
            pg.draw.line(sprite, "0xD0D0D0", (line_x, 0), (line_x, size[1]))
            alph += alph_interval
        pg.draw.rect(sprite, "0xD0D0D0", (0, 0, size[0], size[1]), 1)
        
        if slider.axis == 1:
            sprite = pg.transform.rotate(sprite, 270)
        slider.sprite = sprite
    
    def draw(slider, surf):
        surf.blit(slider.sprite, slider.pos)
