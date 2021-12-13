from random import random
from random import randint
from time import time_ns as nanosec
from math import *
import pygame as pg
import pygame.freetype as ft
from view  import *
from input import *
from rigid import *
from tree  import *
from frame import *
from txter import *

# константы
max_fps = 25
WIDTH = 1600
HIGHT = 800
timescale = 0.00
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((WIDTH, HIGHT+200))
clock = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
frame = Frame()
frame.drag((WIDTH/2, HIGHT/2))
frame.flip_y = True
# инициализация тел
massive_bodies, light_bodies = file_to_bodies("systems/" + "system_2.txt")
all_bodies = massive_bodies | light_bodies
tree = Square_tree()
for body in all_bodies:
    for part in body.part:
        tree.add_elem(part.x, part.y, part.r, part)
# кнопки
btn_screen = Button(0, 0, WIDTH, HIGHT)

slider_screen_x   = Slider( (0, 0), (WIDTH, HIGHT), 0)
slider_screen_y   = Slider( (0, 0), (WIDTH, HIGHT), 1)
slider_frame_alph = Slider( (1100, 960), (150, 30), 0)
slider_timescale  = Slider( (450, 950), (300, 30), 0)

sliders = {slider_screen_x, slider_screen_y, slider_timescale, slider_frame_alph}
# осн цикл
en_0 = Rigid_body.calc_energy (massive_bodies, massive_bodies)
vx_frame, vy_frame = 0, 0
fps = 0
itr = 0
dt = 0
while not finished:
    #model - вычисления симуляции.
    t0 = nanosec()
    Rigid_body.runge_kutta_n_body(massive_bodies, all_bodies, dt*timescale)
    t1 = nanosec()
    for body in all_bodies:
        for part in body.part:
            tree.upd_elem(part.x, part.y, part.r, part)
    intersect = tree.get_intersect()
    for pair in intersect:
        if pair[0].body not in massive_bodies and pair[1].body in massive_bodies:
            Rigid_body.calc_coll_massive (pair[0], pair[1])
        if pair[1].body not in massive_bodies and pair[0].body in massive_bodies:
            Rigid_body.calc_coll_massive (pair[1], pair[massive_bodies, light_bodies0])
        else:
            Rigid_body.calc_coll (pair[0], pair[1])
    if not itr%10:
        tree.trunc_empty() #периодически обрезаем пустые ветки чтобы освобождаать память.
    t2 = nanosec()
    '''
    en = Rigid_body.calc_energy (massive_bodies, massive_bodies)
    if abs(en/en_0 - 1) == 0:
        print ( "None")
    else:
        print ( "{0:+6.2f}".format( math.log(abs(en/en_0 - 1))/math.log(10) ) )
    '''
    #view - отрисовка
    draw_bodies(all_bodies, screen, frame)
    
    font.render_to(screen, (10, HIGHT+50*0), "fps:      {0:6.2f}   itr:{1:4d}".format(fps, itr), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*1), "dt_grav:{0:5d}".format( (t1-t0)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*2), "dt_coll:{0:5d}".format( (t2-t1)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*3), "timescale:{0:5.3f}".format(timescale), (232, 98, 129), (0, 0, 0, 0))
    
    slider_timescale.draw(screen)
    slider_frame_alph.draw(screen)
    #slider_screen_x.draw(screen)       
    #slider_screen_y.draw(screen)
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
    
    #controller - получение информации из внешнего мира
    events = pg.event.get()
    Slider.event_handler(sliders, events)
    for event in events:
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            btn_screen.click(event.pos[0], event.pos[1])
            if btn_screen.state or True:
                if event.button == 4:
                    frame.scale_at_point (event.pos, 1.2)
                if event.button == 5:
                    frame.scale_at_point (event.pos, 0.8)
            btn_screen.state = False
    
    timescale = max(0, timescale + slider_timescale.offset * 0.001)
    frame.drag((slider_screen_x.offset, slider_screen_y.offset))
    frame.rotate_around((WIDTH/2, HIGHT/2), slider_frame_alph.offset * 0.01)
    
    dt = clock.tick(max_fps)/1000
    fps = clock.get_fps()
    itr+=1

bodies_to_file ("systems/" + "autosave.txt", massive_bodies, light_bodies)
ft.quit()
pg.quit()

'''
av_len = 1000
av_line = [0] * av_len
av_i = 0
av_sum = 0
    av_sum -= av_line[av_i]
    av_line[av_i] = dt
    av_sum += av_line[av_i]
    av_i = (av_i + 1)%av_len
'''
