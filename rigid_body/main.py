from random import random
from random import randint
from time import time_ns as nanosec
import pygame as pg
import pygame.freetype as ft
import math
from view import *
from btn import *
from rigid import *
from tree import *
from scale import *

# константы
max_fps = 25
WIDTH = 1600
HIGHT = 800
G = 6.67E-11
f_forward = 0.00
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((WIDTH, HIGHT+200))
clock = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)

frame = Frame()
frame.flip_y = True
# инициализация тел
massive_bodies = set()
light_bodies = set()
all_bodies = set()

for k in range(10):
    n = 1 + round(6*random())
    y_0 = 40*k
    part_set = set()
    for i in range(n):
        part_set.add( Rigid_body.Part_circle(m=1E14, r=5, color="0x008000", x=50 + 0.01*random() + 10 * math.cos(2*math.pi * i/n),  y=y_0 + 10 * math.sin(2*math.pi * i/n)) )
    massive_bodies.add( Rigid_body(part_set, vx=0, vy=0, omeg=0) )

part_set = set()
part_set.add( Rigid_body.Part_circle(m=1E15, r=2, color=(100, 230, 20), x=0, y=0) )
part_set.add( Rigid_body.Part_circle(m=1E10, r=2, color=(230, 100, 20), x=20, y=0) )
part_set.add( Rigid_body.Part_circle(m=1E10, r=2, color=(100, 20, 230), x=0, y=20) )
massive_bodies.add( Rigid_body(part_set, vx=0, vy=0, omeg=0) )


all_bodies = massive_bodies | light_bodies
tree = Square_tree()
for body in all_bodies:
    for part in body.part:
        tree.add_elem(part.x, part.y, part.r, part)
# кнопки
btn_1 = Button(550, HIGHT+50, 150, 100)
btn_spinc = Button(800, HIGHT+50, 50, 50)
btn_spdec = Button(750, HIGHT+50, 50, 50)
btn_screen = Button(0, 0, WIDTH, HIGHT)
# осн цикл
en_0 = Rigid_body.calc_energy (massive_bodies, massive_bodies)

fps = 0
itr = 0
dt = 0
screen_drag = False
while not finished:
    #model - вычисления симуляции.
    
    
    t0 = nanosec()
    Rigid_body.runge_kutta_n_body(massive_bodies, all_bodies, dt*f_forward)
    t1 = nanosec()
    for body in all_bodies:
        for part in body.part:
            tree.upd_elem(part.x, part.y, part.r, part)
    intersect = tree.get_intersect()
    for pair in intersect:
        if pair[0].body not in massive_bodies and pair[1].body in massive_bodies:
            Rigid_body.calc_coll_massive (pair[0], pair[1])
        if pair[1].body not in massive_bodies and pair[0].body in massive_bodies:
            Rigid_body.calc_coll_massive (pair[1], pair[0])
        else:
            Rigid_body.calc_coll (pair[0], pair[1])
    if not itr%10:
        tree.trunc_empty() #периодически обрезаем пустые ветки чтобы освобождаать память.
    t2 = nanosec()
    
    en = Rigid_body.calc_energy (massive_bodies, massive_bodies)
    if abs(en/en_0 - 1) == 0:
        print ( "None")
    else:
        print ( "{0:+6.2f}".format( math.log(abs(en/en_0 - 1))/math.log(10) ) )
    
    #view - отрисовка
    if btn_1.state:
        draw_root(tree.root, screen, frame)
    for body in all_bodies:
        draw_body(body, screen, frame)
    
    font.render_to(screen, (10, HIGHT+50*0), "fps:      {0:6.2f}   itr:{1:4d}".format(fps, itr), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*1), "dt_grav:{0:5d}".format( (t1-t0)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*2), "dt_coll:{0:5d}".format( (t2-t1)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*3), "f_forward:{0:4.2f}".format(f_forward ), (232, 98, 129), (0, 0, 0, 0))
    
    btn_1.draw_butt(screen)
    btn_spinc.draw_butt(screen)
    btn_spdec.draw_butt(screen)
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
    
    #controller - получение информации из внешнего мира
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            btn_1.click(event.pos[0], event.pos[1])
            btn_spinc.click(event.pos[0], event.pos[1])
            btn_spdec.click(event.pos[0], event.pos[1])
            if btn_spinc.state:
                f_forward += 0.10
            if btn_spdec.state:
                f_forward = max(f_forward-0.10, 0)
            
            btn_screen.click(event.pos[0], event.pos[1])
            if btn_screen.state and event.button == 1:
                screen_drag = True
            if btn_screen.state or True:
                if event.button == 4:
                    frame.scale_at_point (event.pos, 1.2)
                if event.button == 5:
                    frame.scale_at_point (event.pos, 0.8)
            
            btn_spdec.state = False
            btn_spinc.state = False
            btn_screen.state = False
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                screen_drag = False
        elif event.type == pg.MOUSEMOTION:
            if screen_drag:
                frame.drag(event.rel)
    
    dt = clock.tick(max_fps)/1000
    fps = clock.get_fps()
    itr+=1
	
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
