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
max_fps = 30
WIDTH = 1800
HIGHT = 1000
timescale = 0.00
# инициализация визуализации
pg.init()
ft.init()
screen = pg.display.set_mode((WIDTH, HIGHT))
clock = pg.time.Clock()
finished = False
font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
small_font = ft.Font(file="Anonymous_Pro.ttf", size=30, font_index=0, resolution=0, ucs4=False)
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
button_screen = Button( (20, 50), (1500, 700) )
button_add    = Button( (1530, 310), (100, 60) )
button_subset = Button( (1630, 310), (50, 60) )
button_cancel = Button( (1710, 310), (50, 60) )

button_select = Button( (1000, 800), (100, 80) )
button_copy   = Button( (1150, 800), (100, 80) )
button_delete = Button( (1250, 800), (100, 80) )

button_draw_lines = Button( (1600, 950), (200, 40) )
buttons = {button_add, button_subset, button_cancel, button_select, button_copy, button_delete, button_draw_lines}

wheel_add_r    = Wheel( (1530, 100), (100, 30), 0, 0)
wheel_add_g    = Wheel( (1530, 150), (100, 30), 0, 0)
wheel_add_b    = Wheel( (1530, 200), (100, 30), 0, 0)
add_color = (wheel_add_r.input_tot, wheel_add_g.input_tot, wheel_add_b.input_tot)
wheel_add_dir  = Wheel( (1530, 420), (100, 30), 0, 0)
wheel_add_omeg = Wheel( (1530, 460), (100, 30), 0, 0)

wheel_screen_x   = Wheel( button_screen.pos, button_screen.size, 0, 0, True)
wheel_screen_y   = Wheel( button_screen.pos, button_screen.size, 1, 0, True)
wheel_timescale  = Wheel( (460, 950), (300, 30), 0)
wheel_frame_alph = Wheel( (800, 950), (150, 30), 0)
wheels = {wheel_screen_x, wheel_screen_y, wheel_timescale, wheel_frame_alph, wheel_add_r, wheel_add_g, wheel_add_b, wheel_add_dir, wheel_add_omeg}

text_rad = Text((1530, 250), (160, 25), small_font, 10)
text_m   = Text((1530, 280), (160, 25), small_font, 10)
text_v   = Text((1530, 380), (160, 25), small_font, 10)
texts = {text_rad, text_m, text_v}
# осн цикл
fps = 0
itr = 0
dt = 0

add_part_set = set()
add_vx = 0
add_vy = 0
while not finished:
    #вычисления модели.
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
            Rigid_body.calc_coll_massive (pair[1], pair[0])
        else:
            Rigid_body.calc_coll (pair[0], pair[1])
    if not itr%10:
        tree.trunc_empty() #периодически обрезаем пустые ветки чтобы освобождаать память.
    t2 = nanosec()
    #отрисовка
    draw_bodies(all_bodies, screen, frame, drawlines=button_draw_lines.input)
    draw_pseudobody(add_part_set, add_vx, add_vy, screen, frame)
    
    font.render_to(screen, (50, 800), "fps:      {0:6.2f}   itr:{1:4d}".format(fps, itr), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (50, 850), "dt_grav:{0:5d}".format( (t1-t0)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (50, 900), "dt_coll:{0:5d}".format( (t2-t1)//1000000 ), (232, 98, 129), (0, 0, 0, 0))
    font.render_to(screen, (50, 950), "timescale:{0:5.3f}".format(timescale), (232, 98, 129), (0, 0, 0, 0))
    
    Button.draw_all(buttons, screen)
    Wheel.draw_all(wheels, screen)
    Text.draw_all(texts, screen)
    
    font.render_to(screen, (1650, 100), "{0:3d}".format(add_color[0]), (255, 0, 0), (0, 0, 0, 0))
    font.render_to(screen, (1650, 150), "{0:3d}".format(add_color[1]), (0, 255, 0), (0, 0, 0, 0))
    font.render_to(screen, (1650, 200), "{0:3d}".format(add_color[2]), (0, 0, 255), (0, 0, 0, 0))
    pg.draw.rect(screen, add_color, (1740, 100, 50, 130))
    pg.draw.rect(screen, "0xFFFFFF", (1740, 100, 50, 130), 1)
    font.render_to(screen, (1730, 250), "r", "0xA0A0A0", (0, 0, 0, 0))
    font.render_to(screen, (1730, 280), "m", "0xA0A0A0", (0, 0, 0, 0))
    font.render_to(screen, (1730, 380), "v", "0xA0A0A0", (0, 0, 0, 0))
    small_font.render_to(screen, (1635, 420), "dir",  "0xA0A0A0", (0, 0, 0, 0))
    small_font.render_to(screen, (1635, 460), "omeg:{0:5.2f}".format(wheel_add_omeg.input_tot*0.01), "0xA0A0A0", (0, 0, 0, 0))
    
    pg.display.update()
    screen.fill((0, 0, 0), (0, 0, WIDTH, HIGHT+200))
    
    #получение информации из внешнего мира
    events = pg.event.get()
    Button.event_handler(buttons, events)
    Wheel.event_handler(wheels, events)
    Text.event_handler(texts, events)
    for event in events:
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:        
            if event.button == 4:
                frame.scale_at_point (event.pos, 1.25)
            if event.button == 5:
                frame.scale_at_point (event.pos, 0.8)
            button_screen.click(event.pos)
            if button_add.input and button_screen.input and event.button == 1:
                x_click, y_click = frame.inverse(event.pos)
                add_part_set.add( Rigid_body.Part_circle(m=add_m, r=add_r, color=add_color, x=x_click, y=y_click) )
        elif event.type == pg.MOUSEMOTION:
            pass
    
    timescale = max(0, timescale + wheel_timescale.input * 0.001)
    frame.rotate_around((WIDTH/2, HIGHT/2), wheel_frame_alph.input * 0.01)
    frame.drag((wheel_screen_x.input, wheel_screen_y.input))
    
    if button_cancel.input:
       button_cancel.input = False
       button_add.input = False
       add_body = None
    
    wheel_add_r.input_tot = max(0, min(wheel_add_r.input_tot, 255))
    wheel_add_g.input_tot = max(0, min(wheel_add_g.input_tot, 255))
    wheel_add_b.input_tot = max(0, min(wheel_add_b.input_tot, 255))
    add_color = (wheel_add_r.input_tot, wheel_add_g.input_tot, wheel_add_b.input_tot)
    if button_add.input:
        if len(text_m.input):
            add_m = float(text_m.input)
        if len(text_rad.input):
            add_r = float(text_rad.input)
        if len(text_v.input):
            add_v = float(text_v.input)
            add_vx = add_v * cos(wheel_add_dir.input_tot*0.01)
            add_vy = add_v * sin(wheel_add_dir.input_tot*0.01)
    elif button_add.input_prev and len(add_part_set):
        new_body = Rigid_body(add_part_set, add_vx, add_vy, wheel_add_omeg.input_tot*0.01)
        all_bodies.add(new_body)
        if button_subset:
            massive_bodies.add(new_body)
        else:
            light_bodies.add(new_body)
        for part in new_body.part:
            tree.add_elem(part.x, part.y, part.r, part)
        add_part_set = set()
        
    for button in buttons:
        button.input_prev = button.input
    
    button_screen.input = False
    dt = clock.tick(max_fps)/1000
    fps = clock.get_fps()
    itr+=1

bodies_to_file ("systems/" + "autosave.txt", massive_bodies, light_bodies)
ft.quit()
pg.quit()
