"""
в данном модуле расположены главные циклы состояний игры - sandbox, saves

класс
    Game_state

функции
    sandbox_loop()
    saves_loop()
"""

from random import random
from random import randint
from time import time_ns as nanosec
from os import listdir
from math import *
import pygame as pg
import pygame.freetype as ft
from view import *
from input import *
from rigid import *
from tree import *
from frame import *
from txter import *

class Game_state:
    """
    класс в объекте которого хранятся основные параметры и объекты игры - размеры и объект поверхности экрана, настройки, конфигурация кнопок
    """
    FINISHED = 0
    SANDBOX = 1
    SAVES = 2
    HELP = 3

    def __init__(game):
        game.state = Game_state.SANDBOX
        pg.init()
        game.MAX_FPS = 40
        game.WIDTH = 1800
        game.HEIGHT = 1000
        game.SIZE = (game.WIDTH, game.HEIGHT)
        game.screen = pg.display.set_mode(game.SIZE)
        game.clock = pg.time.Clock()
        ft.init()
        game.font = ft.Font(
            file="Anonymous_Pro.ttf",
            size=50,
            font_index=0,
            resolution=0,
            ucs4=False)

    def quit(game):
        ft.quit()
        pg.quit()

    #button_start_sprite = pg.image.load("sprites/button_start.png").convert()

def sandbox_loop(game, BACK):
    small_font = ft.Font(
        file="Anonymous_Pro.ttf",
        size=30,
        font_index=0,
        resolution=0,
        ucs4=False)
    frame = Frame()
    frame.drag((game.WIDTH / 2, game.HEIGHT / 2))
    frame.flip_y = True

    massive_bodies, light_bodies = file_to_bodies("saves/" + "system_0.txt")
    all_bodies = massive_bodies | light_bodies
    tree = Square_tree()
    for body in all_bodies:
        for part in body.part:
            tree.add_elem(part.x, part.y, part.r, part)
    # загрузка спрайтов
    button_back_sprite = pg.image.load("sprites/button_back.png").convert()
    button_saves_sprite = pg.image.load("sprites/button_saves.png").convert()
    button_add_sprite_0 = pg.image.load("sprites/button_add_0.png").convert()
    button_add_sprite_1 = pg.image.load("sprites/button_add_1.png").convert()
    button_cancel_sprite = pg.image.load("sprites/button_cancel.png").convert()
    button_subset_sprite_0 = pg.image.load("sprites/button_subset_0.png").convert()
    button_subset_sprite_1 = pg.image.load("sprites/button_subset_1.png").convert()
    button_draw_lines_sprite_0 = pg.image.load("sprites/draw_lines_0.png").convert()
    button_draw_lines_sprite_1 = pg.image.load("sprites/draw_lines_1.png").convert()
    # Инициализация элементов интерфейса
    button_saves = Button((30, 5), (40, 40), button_saves_sprite)
    button_screen = Button((20, 50), (1500, 800), sprite_1=Button.get_whitebox_0((1500, 700)))
    button_add = Button((1530, 310), (100, 60), button_add_sprite_0, button_add_sprite_1)
    button_subset = Button((1630, 310), (50, 60), button_subset_sprite_0, button_subset_sprite_1)
    button_cancel = Button((1710, 310), (50, 60), button_cancel_sprite)
    '''
    button_select = Button((1000, 800), (100, 80))
    button_copy = Button((1150, 800), (100, 80))
    button_delete = Button((1250, 800), (100, 80))
    '''
    button_draw_lines = Button((1530, 550), (200, 40), button_draw_lines_sprite_0, button_draw_lines_sprite_1)
    buttons = {
        button_saves,
        button_screen,
        button_add,
        button_subset,
        button_cancel,
        button_draw_lines}

    wheel_add_r = Wheel((1530, 100), (100, 30), 0, 0)
    wheel_add_g = Wheel((1530, 150), (100, 30), 0, 0)
    wheel_add_b = Wheel((1530, 200), (100, 30), 0, 0)
    add_color = (
        wheel_add_r.input_tot,
        wheel_add_g.input_tot,
        wheel_add_b.input_tot)
    wheel_add_dir = Wheel((1530, 420), (100, 30), 0, 0)
    wheel_add_omeg = Wheel((1530, 460), (100, 30), 0, 0)

    wheel_screen_x = Wheel(button_screen.pos, button_screen.size, 0, 0, True)
    wheel_screen_y = Wheel(button_screen.pos, button_screen.size, 1, 0, True)
    wheel_timescale = Wheel((460, 950), (300, 30), 0)
    wheel_frame_alph = Wheel((800, 950), (150, 30), 0)
    wheels = {
        wheel_screen_x,
        wheel_screen_y,
        wheel_timescale,
        wheel_frame_alph,
        wheel_add_r,
        wheel_add_g,
        wheel_add_b,
        wheel_add_dir,
        wheel_add_omeg}

    text_rad = Text((1530, 250), (160, 25), small_font, 10)
    text_m = Text((1530, 280), (160, 25), small_font, 10)
    text_v = Text((1530, 380), (160, 25), small_font, 10)
    texts = {text_rad, text_m, text_v}
    # вспомогательные переменные
    fps = 0
    itr = 0
    dt = 0
    timescale = 0.00

    add_part_set = set()
    add_vx = 0
    add_vy = 0
    add_m = 1
    add_r = 10
    while game.state == Game_state.SANDBOX:
        # model
        Rigid_body.runge_kutta_n_body(
            massive_bodies, all_bodies, dt * timescale)

        for body in all_bodies:
            for part in body.part:
                tree.upd_elem(part.x, part.y, part.r, part)
        intersect = tree.get_intersect()
        for pair in intersect:
            if pair[0].body not in massive_bodies and pair[1].body in massive_bodies:
                Rigid_body.calc_coll_massive(pair[0], pair[1])
            if pair[1].body not in massive_bodies and pair[0].body in massive_bodies:
                Rigid_body.calc_coll_massive(pair[1], pair[0])
            else:
                Rigid_body.calc_coll(pair[0], pair[1])

        if not itr % 10:
            # периодически обрезаем пустые ветки чтобы освобождаать память.
            tree.trunc_empty()
        # view
        draw_bodies(all_bodies, game.screen, frame, drawlines=button_draw_lines.input)
        draw_pseudobody(add_part_set, add_vx, add_vy, game.screen, frame)

        game.font.render_to(game.screen, (50, 900), "fps:{0:6.2f}   itr:{1:4d}".format(fps, itr), "0xA0A0A0", (0, 0, 0, 0))
        game.font.render_to(game.screen, (50, 950), "timescale:{0:5.3f}".format(timescale), "0xA0A0A0", (0, 0, 0, 0))

        Button.draw_all(buttons, game.screen)
        Wheel.draw_all(wheels, game.screen)
        Text.draw_all(texts, game.screen)

        game.font.render_to(game.screen, (1650, 100), "{0:3d}".format(add_color[0]), (255, 0, 0), (0, 0, 0, 0))
        game.font.render_to(game.screen, (1650, 150), "{0:3d}".format(add_color[1]), (0, 255, 0), (0, 0, 0, 0))
        game.font.render_to(game.screen, (1650, 200), "{0:3d}".format(add_color[2]), (0, 0, 255), (0, 0, 0, 0))
        pg.draw.rect(game.screen, add_color, (1740, 100, 50, 130))
        pg.draw.rect(game.screen, "0xFFFFFF", (1740, 100, 50, 130), 1)
        game.font.render_to(game.screen, (1730, 250), "r", "0xA0A0A0", (0, 0, 0, 0))
        game.font.render_to(game.screen, (1730, 280), "m", "0xA0A0A0", (0, 0, 0, 0))
        game.font.render_to(game.screen, (1730, 380), "v", "0xA0A0A0", (0, 0, 0, 0))
        small_font.render_to(game.screen, (1635, 420), "dir", "0xA0A0A0", (0, 0, 0, 0))
        small_font.render_to(game.screen, (1635, 460), "omeg:{0:5.2f}".format(wheel_add_omeg.input_tot * 0.01), "0xA0A0A0", (0, 0, 0, 0))

        pg.display.update()
        game.screen.fill("0x000000")
        # Обработка событий
        events = pg.event.get()
        Button.event_handler(buttons, events)
        Wheel.event_handler(wheels, events)
        Text.event_handler(texts, events)
        for event in events:
            if event.type == pg.QUIT:
                game.state = Game_state.FINISHED
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    frame.scale_at_point(event.pos, 1.25)
                if event.button == 5:
                    frame.scale_at_point(event.pos, 0.8)
                if button_add.input and button_screen.input and event.button == 1:
                    x_click, y_click = frame.inverse(event.pos)
                    add_part_set.add(
                        Rigid_body.Part_circle(
                            m=add_m,
                            r=add_r,
                            color=add_color,
                            x=x_click,
                            y=y_click))
            elif event.type == pg.MOUSEMOTION:
                pass

        timescale = max(0, timescale + wheel_timescale.input * 0.001)
        frame.rotate_around(
            (game.WIDTH / 2,
             game.HEIGHT / 2),
            wheel_frame_alph.input * 0.01)
        frame.drag((wheel_screen_x.input, wheel_screen_y.input))

        if button_cancel.input:
            button_cancel.input = False
            button_add.input = False
            add_part_set = set()

        wheel_add_r.input_tot = max(0, min(wheel_add_r.input_tot, 255))
        wheel_add_g.input_tot = max(0, min(wheel_add_g.input_tot, 255))
        wheel_add_b.input_tot = max(0, min(wheel_add_b.input_tot, 255))
        add_color = (
            wheel_add_r.input_tot,
            wheel_add_g.input_tot,
            wheel_add_b.input_tot)
        if button_add.input:
            if len(text_m.input):
                add_m = float(text_m.input)
            if len(text_rad.input):
                add_r = float(text_rad.input)
            if len(text_v.input):
                add_v = float(text_v.input)
                add_vx = add_v * cos(wheel_add_dir.input_tot * 0.01)
                add_vy = add_v * sin(wheel_add_dir.input_tot * 0.01)
        elif button_add.input_prev and len(add_part_set):
            new_body = Rigid_body(
                add_part_set,
                add_vx,
                add_vy,
                wheel_add_omeg.input_tot *
                0.01)
            all_bodies.add(new_body)
            if button_subset.input:
                massive_bodies.add(new_body)
            else:
                light_bodies.add(new_body)
            for part in new_body.part:
                tree.add_elem(part.x, part.y, part.r, part)
            add_part_set = set()

        if button_saves.input:
            game.state = Game_state.SAVES
            saves_loop(game, Game_state.SANDBOX)
            button_saves.input = False

        for button in buttons:
            button.input_prev = button.input

        button_screen.input = False
        dt = game.clock.tick(game.MAX_FPS) / 1000
        fps = game.clock.get_fps()
        itr += 1


def saves_loop(game, BACK):
    # загрузка спрайтов
    button_back_sprite = pg.image.load("sprites/button_back.png").convert()
    # Инициализация кнопок
    button_back = Button((30, 5), (40, 40), button_back_sprite)
    buttons = {button_back}
    wheels = {}
    while game.state == Game_state.SAVES:
        # model

        # view
        button_back.draw(game.screen)
        pg.display.update()
        game.screen.fill("0x000000")

        # controller
        events = pg.event.get()
        Button.event_handler(buttons, events)
        Wheel.event_handler(wheels, events)
        for event in events:
            if event.type == pg.QUIT:
                game.state = Game_state.FINISHED

        if button_back.input:
            game.state = BACK

        game.clock.tick(game.MAX_FPS)
        fps = game.clock.get_fps()

if __name__ == "__main__":
    print("This module is not for direct call!")
