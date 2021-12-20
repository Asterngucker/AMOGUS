import pygame as pg
from math import *

# В этом модуле описаны объекты для ввода информации со стороны игрока - кнопка, колёсико и (FIXME окно ввода текста)

class Button:
    def __init__ (button, pos, size, sprite_0 = None, sprite_1 = None, nosprite = False):
        button.pos        = pos
        button.size       = size
        if not nosprite:
            button.sprite_0 = sprite_0 if sprite_0 is not None else Button.get_whitebox_0(size)
            button.sprite_1 = sprite_1 if sprite_1 is not None else Button.get_whitebox_1(size)
        button.input      = False
        button.input_prev = False
        button.nosprite   = nosprite
    
	#белые коробки - спрайты по умолчанию
    @staticmethod
    def get_whitebox_0(size):
        whitebox_0 = pg.Surface(size)
        whitebox_0.set_colorkey("0x000000")
        pg.draw.lines(whitebox_0, "0xD0D0D0", True,  [(0, 0), (size[0]-1, 0), (size[0]-1, size[1]-1), (0, size[1]-1)] )
        return whitebox_0
    
    @staticmethod
    def get_whitebox_1(size):
        whitebox_1 = Button.get_whitebox_0(size)
        pg.draw.line(whitebox_1, "0xD0D0D0", (0, 0), (size[0]-1, size[1]-1))
        pg.draw.line(whitebox_1, "0xD0D0D0", (size[0]-1, 0), (0, size[1]-1))
        return whitebox_1
    
    def click (button, click_pos):
    	#меняет состояние при попадании по кнопке
        if (button.pos[0] < click_pos[0]) and (button.pos[0] + button.size[0] > click_pos[0]) and (button.pos[1] < click_pos[1]) and (button.pos[1] + button.size[1] > click_pos[1]):
            button.input = not button.input
    
    @staticmethod
    def event_handler (buttons, events): #Проверяет все кнопки на нажатие.
        #for button in buttons:
        #    button.input = 0
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.click(event.pos)
    
    def draw (button, surface):
        if not button.nosprite:
            if button.input:
                if button.size != button.sprite_1.get_size():
                    button.sprite_1 = pg.transform.smoothscale(button.sprite_1, button.size)
                surface.blit(button.sprite_1, button.pos)
            else:
                if button.size != button.sprite_0.get_size():
                    button.sprite_0 = pg.transform.smoothscale(button.sprite_0, button.size) 
                surface.blit(button.sprite_0, button.pos)
    
    @staticmethod
    def draw_all(buttons, surface):
        for button in buttons:
            button.draw(surface)


class Wheel:
    '''
    крутилка, на которую можно нажать ЛКМ и потянуть мышкой.
    Вертикальная или горизонтальная, произвольный прямоугольник экранных осей.
    В wheel.input пишет смещение за кадр. 0 если не нажата.
    wheel.input_tot - суммирующееся смещение.
    '''
    def __init__(wheel, pos, size, axis, input_tot = 0, nosprite = False):
        '''
        **pos**  — положение верхнего левого угла
        **size** — размер
        **axis** — ось: 0==x, 1==y
        '''
        wheel.pos         = pos
        wheel.size        = size
        wheel.pressed     = False
        wheel.input       = 0
        wheel.input_tot   = input_tot
        wheel.axis        = axis
        wheel.nosprite    = nosprite
        if not nosprite:
            wheel.sprite  = None
            wheel.upd_sprite()  
    
    def click (wheel, pos):
        if wheel.pos[0] < pos[0] and wheel.pos[0]+wheel.size[0] > pos[0] and wheel.pos[1] < pos[1] and wheel.pos[1]+wheel.size[1] > pos[1]:
            wheel.pressed = True
    
    def drag (wheel, rel):
        if wheel.pressed:
            wheel.input     += rel[wheel.axis]
            wheel.input_tot += rel[wheel.axis]
            if not wheel.nosprite:
                wheel.upd_sprite()
    
    def release (wheel):
        if wheel.pressed:
            wheel.pressed = False
    
    @staticmethod
    def event_handler (wheels, events): #Проверяет все события на всех крутилках. В список wheels стоит добавить все активные крутилки.
        for wheel in wheels:
            wheel.input = 0
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for wheel in wheels:
                    wheel.click(event.pos)
            elif event.type == pg.MOUSEMOTION:
                for wheel in wheels:
                    wheel.drag(event.rel)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for wheel in wheels:
                    wheel.release()
    
    def upd_sprite (wheel): 
        if wheel.axis == 1:
            size = (wheel.size[1], wheel.size[0])
        else:
            size = wheel.size
        sprite = pg.Surface(size)
        sprite.set_colorkey("0x000000")
        r = size[0]*0.5                                      #радиус колёсика. Отрисовывается вид с ребра.
        alph_interval = 0.15                                 #расстояние между рисками в радианах
        delta_dash = wheel.input_tot/(r*alph_interval)
        alph_input = (delta_dash - round(delta_dash-0.5)) * alph_interval
        alph_0 = asin(size[0]/(2*r))
        alph = -alph_0 + alph_input
        while alph < alph_0:
            line_x = size[0]/2 + r*sin(alph)
            pg.draw.line(sprite, "0xD0D0D0", (line_x, 0), (line_x, size[1]))
            alph += alph_interval
        pg.draw.rect(sprite, "0xD0D0D0", (0, 0, size[0], size[1]), 1)
        
        if wheel.axis == 1:
            sprite = pg.transform.rotate(sprite, 270)
        wheel.sprite = sprite
    
    def draw(wheel, surf):
        if not wheel.nosprite:
            surf.blit(wheel.sprite, wheel.pos)
    
    @staticmethod
    def draw_all(wheels, surface):
        for wheel in wheels:
            wheel.draw(surface)

class Text:
    '''
    
    '''
    def __init__(text, pos, size, font, max_len):
        text.pos     = pos
        text.size    = size
        text.font    = font
        text.pressed = False
        text.input   = ""
        text.buffer  = ""
        text.max_len = max_len
   
    def click (text, pos):
        if text.pos[0] < pos[0] and text.pos[0]+text.size[0] > pos[0] and text.pos[1] < pos[1] and text.pos[1]+text.size[1] > pos[1]:
            text.pressed = True
            text.buffer = text.input
    
    @staticmethod
    def event_handler (texts, events):
        for event in events:
            for text in texts:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    text.click(event.pos)
                if text.pressed:
                    if event.type == pg.TEXTINPUT and event.text != pg.K_SPACE and len(text.buffer)<text.max_len:
                        text.buffer += event.text
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            text.buffer = text.buffer[0:len(text.buffer)-1]
                        elif event.key == pg.K_RETURN:
                            text.input = text.buffer
                            text.buffer = ""
                            text.pressed = False
                        elif event.key == pg.K_ESCAPE:
                            text.buffer = ""
                            text.pressed = False
    
    def draw(text, surface):
        tmp_surf = pg.Surface(text.size)
        if text.pressed:
            text.font.render_to(tmp_surf, (0, 0), text.buffer + "_", "0xFFFFFF", (0, 0, 0, 0))
        else:
            text.font.render_to(tmp_surf, (0, 0), text.input,  "0xFFFFFF", (0, 0, 0, 0))
        pg.draw.rect(tmp_surf, "0xFFFFFF", (0, 0, text.size[0], text.size[1]), 1)
        surface.blit(tmp_surf, text.pos)
    
    @staticmethod
    def draw_all(texts, surface):
        for text in texts:
            text.draw(surface)
