#в данном модуле расположены главные циклы состояний игры - menu, sandbox, save_menu, help, settings

from random import random
from random import randint
from time import time_ns as nanosec
from math import *
import pygame as pg
import pygame.freetype as ft

from input import *


class Game_state:
    '''
    класс в объекте которого хранятся основные параметры и глобальные объекты игры - размеры и объект поверхности экрана, настройки, конфигурация кнопок
    '''
    FINISHED  = 0
    MENU      = 1
    SANDBOX   = 2
    SAVES     = 3
    HELP      = 4
    SETTINGS  = 5
    
    def __init__(game):
        game.state = Game_state.MENU
        
        pg.init()
        game.MAX_FPS = 40
        game.WIDTH   = 1600
        game.HIGHT   = 1000
        game.SIZE    = (game.WIDTH, game.HIGHT)
        game.screen  = pg.display.set_mode(game.SIZE)
        game.clock   = pg.time.Clock()
        
        ft.init()
        game.font = ft.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
    
    def quit(game):
        ft.quit()
        pg.quit()
        

def menu_loop(game, BACK): #описывает цикл главного меню игры
    #загрузка спрайтов
    button_start_sprite = pg.image.load("sprites/button_start.png").convert()
    #Инициализация кнопок
    button_start    = Button ((600, 300), (400, 100), button_start_sprite)
    button_settings = Button ((650, 520), (300, 80))
    button_help     = Button ((650, 620), (300, 80))
    buttons = {button_start, button_settings, button_help}    
    while game.state == Game_state.MENU:
        #model
        
        #view
        button_start.draw(game.screen)
        button_settings.draw(game.screen)
        button_help.draw(game.screen)
        
        pg.display.update()
        game.screen.fill("0x000000")
        
        #controller
        events = pg.event.get()
        Button.event_handler(buttons, events)
        for event in events:
            if event.type == pg.QUIT:
                game.state = Game_state.FINISHED
        
        if button_start.input:
            game.state = Game_state.SANDBOX
            sandbox_loop(game, Game_state.MENU)
            button_start.input = False
        if button_settings.input:
            game.state = Game_state.SETTINGS
            settings_loop(game, Game_state.MENU)
            button_settings.input = False
        if button_help.input:
            game.state = Game_state.HELP
            help_loop(game, Game_state.MENU)
            button_help.input = False
        
        game.clock.tick(game.MAX_FPS)
        fps = game.clock.get_fps()



def sandbox_loop(game, BACK):
    view_screen = pg.Surface( (1200, 700) )
    #загрузка спрайтов
    
    #Инициализация кнопок
    button_back     = Button (( 10, 10), ( 40, 40))
    button_settings = Button (( 50, 10), ( 40, 40))
    button_help     = Button (( 90, 10), ( 40, 40))
    button_saves    = Button ((150, 10), (100, 40))
    buttons = {button_back, button_settings, button_help, button_saves}
    wheels = {}
    while game.state == Game_state.SANDBOX:
        #model
        
        #view
        button_back.draw(game.screen)
        button_settings.draw(game.screen)
        button_help.draw(game.screen)
        button_saves.draw(game.screen)
        pg.draw.rect(game.screen, "0xD0D0D0", (100, 100, view_screen.get_width(), view_screen.get_height()), 1)
        
        pg.display.update()
        game.screen.fill("0x000000")
        view_screen.fill("0x000000")
        #controller
        events = pg.event.get()
        Button.event_handler(buttons, events)
        Wheel.event_handler(wheels, events)
        for event in events:
            if event.type == pg.QUIT:
                game.state = Game_state.FINISHED
        
        if button_back.input:
            game.state = BACK
        if button_settings.input:
            game.state = Game_state.SETTINGS
            settings_loop (game, Game_state.SANDBOX)
            button_settings.input = False
        if button_help.input:
            game.state = Game_state.HELP
            help_loop (game, Game_state.SANDBOX)
            button_help.input = False
        if button_saves.input:
            game.state = Game_state.SAVES
            saves_loop (game, Game_state.SANDBOX)
            button_saves.input = False
        
        game.clock.tick(game.MAX_FPS)
        fps = game.clock.get_fps()

def saves_loop(game, BACK):
    print(BACK)
    #загрузка спрайтов
    
    #Инициализация кнопок
    button_back = Button (( 10, 10), ( 40, 40))
    buttons = {button_back}
    wheels = {}
    while game.state == Game_state.SAVES:
        #model
        
        #view
        button_back.draw(game.screen)
        pg.display.update()
        game.screen.fill("0x000000")
        
        #controller
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

def help_loop(game, BACK):
    #загрузка спрайтов
    
    #Инициализация кнопок
    button_back = Button ((10, 10), (40, 40))
    buttons = {button_back}
    wheels = {}
    while game.state == Game_state.HELP:
        #model
        
        #view
        button_back.draw(game.screen)
        
        pg.display.update()
        game.screen.fill("0x000000")
        
        #controller
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

def settings_loop(game, BACK):
    #загрузка спрайтов
    
    #Инициализация кнопок
    button_back = Button ((10, 10), (40, 40))
    buttons = {button_back}
    wheels = {}
    while game.state == Game_state.SETTINGS:
        #model
        
        #view
        button_back.draw(game.screen)
        
        pg.display.update()
        game.screen.fill("0x000000")
        
        #controller
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
    print("This module is NOT for direct call!")
