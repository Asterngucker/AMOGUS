from random import random
from random import randint
from time import time_ns as nanosec
import pygame as pg
import pygame.freetype as ft
import math
from btn import *
from rigid import *
from tree import *

def draw_root (root, screen):
    if root.light:# or True:
        if len(root.gas)!=0:
            pg.draw.rect (screen, (40, 130, 200), (root.x-root.r, root.y-root.r, 2*root.r, 2*root.r))
        pg.draw.rect (screen, (200, 200, 200), (root.x-root.r, root.y-root.r, 2*root.r, 2*root.r), 1)
        if root.child_lu is not None:
            root.child_lu.draw_root(screen)
        if root.child_ru is not None:
            root.child_ru.draw_root(screen)
        if root.child_rd is not None:
            root.child_rd.draw_root(screen)
        if root.child_ld is not None:
            root.child_ld.draw_root(screen)

Tree_root.draw_root = draw_root

# константы
max_fps = 40
WIDTH = 1600
HIGHT = 800
g = -40
f_forward = 0.50
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((WIDTH, HIGHT+200))
clock = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
# инициализация тел
gas = set()

n = 80
part_set = set()
for i in range(n):
    part_set.add( Rigid_body.Part_circle(m=1/n, r=20, color=(20, 130, 20), x=WIDTH/2 + 250*math.sin(2*math.pi * i/n),  y=HIGHT/2 - 2000 + 100*math.cos(2*math.pi * i/n)) )
part_set.add( Rigid_body.Part_circle(m=20,  r=40, color=(20, 130, 20), x=WIDTH/2-60, y=HIGHT/2 + 100 - 2000) )
part_set.add( Rigid_body.Part_circle(m=90,  r=60, color=(20, 130, 20), x=WIDTH/2,    y=HIGHT/2 + 120 - 2000) )
part_set.add( Rigid_body.Part_circle(m=20,  r=40, color=(20, 130, 20), x=WIDTH/2+60, y=HIGHT/2 + 100 - 2000) )
gas.add( Rigid_body(part_set, vx=0, vy=0, omeg=0) )
part_set = set()

for i in range (300):
    n = round(1+7*random())
    x_0=WIDTH*(0.1+0.8*random())
    y_0=HIGHT*(0.8+0.1*random())
    part_set = set()
    for i in range(n):
        part_set.add( Rigid_body.Part_circle(m=1/n, r=5, color=(200, 130, 20), x=x_0 + 15*math.sin(2*math.pi * i/n),  y=y_0 + 15*math.cos(2*math.pi * i/n)) )
    gas.add( Rigid_body(part_set, vx=0, vy=0, omeg=0) )

tree = Square_tree()
for body in gas:
    for part in body.part:
        tree.add_elem(part.x, part.y, part.r, part)

bound_r = 20000
part_set = set()
#part_set.add( Rigid_body.Part_circle(m=1E7, r=bound_r, color=(50, 50, 140), x=WIDTH/2, y=-bound_r) )
part_set.add( Rigid_body.Part_circle(m=1E7, r=bound_r, color=(50, 50, 140), x=WIDTH+bound_r, y=HIGHT/2) )
part_set.add( Rigid_body.Part_circle(m=1E7, r=bound_r, color=(50, 50, 140), x=WIDTH/2, y=HIGHT+bound_r) )
part_set.add( Rigid_body.Part_circle(m=1E7, r=bound_r, color=(50, 50, 140), x=-bound_r, y=HIGHT/2) )
bound = Rigid_body(part_set, vx=0, vy=0, omeg=0)

for part in bound.part:
    tree.add_elem(part.x, part.y, part.r, part)
# кнопки
btn_1 = Button(550, HIGHT+50, 150, 100)
btn_spinc = Button(800, HIGHT+50, 50, 50)
btn_spdec = Button(750, HIGHT+50, 50, 50)
# осн цикл
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
fps = 0
itr = 0
dt = 0
while not finished:
    if btn_spinc.state:
        f_forward += 0.05
        btn_spinc.state = False
    if btn_spdec.state:
        f_forward = max(f_forward-0.04, 0)
        btn_spdec.state = False
    
    bound.move_dt(dt*f_forward, 0)
    for body in gas:
        body.move_dt(dt*f_forward, g)
    
    t0 = nanosec()
    for part in bound.part:
        tree.upd_elem(part.x, part.y, part.r, part)
    for body in gas:
        for part in body.part:
            tree.upd_elem(part.x, part.y, part.r, part)
    intersect = tree.get_intersect()
    for pair in intersect:
        part_1 = pair[0]
        part_2 = pair[1]
        if part_1.body is not part_2.body:
            Rigid_body.calc_coll (part_1, part_2)
    t1 = nanosec()
    
    if btn_1.state:
        tree.root.draw_root(screen)
    bound.draw_body(screen)
    for body in gas:
        body.draw_body(screen)
    
    font.render_to(screen, (10, HIGHT+50*0), "fps:      {0:6.2f}   itr:{1:4d}".format(fps, itr), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*1), "dt_coll:{0:5d}".format( (t1-t0)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    #font.render_to(screen, (10, HIGHT+50*2), "dt_draw:    {0:4d}".format(dt_draw   ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (10, HIGHT+50*3), "f_forward:{0:4.2f}".format(f_forward ), (232, 98, 129), (0, 0, 0, 0))
    
    btn_1.draw_butt(screen)
    btn_spinc.draw_butt(screen)
    btn_spdec.draw_butt(screen)
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
	
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            btn_1.click(event.pos[0], event.pos[1])
            btn_spinc.click(event.pos[0], event.pos[1])
            btn_spdec.click(event.pos[0], event.pos[1])
            
    dt = clock.tick(max_fps)/1000
    fps = clock.get_fps()
    itr+=1
	
ft.quit()
pg.quit()
