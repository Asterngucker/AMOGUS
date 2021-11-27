import pygame, math
from pygame import *
from math import *

pygame.init()

#создаем окно
WIN_WIDTH = 800
WIN_HEIGHT = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Solar System")

SPACE_COLOR = "#000022"
 
timer = pygame.time.Clock()

#класс объектов планета
class Planet:
    G = 6.67 * 10**(-11)
    def __init__(self, name, m, r, color, x, y, vx, vy, sputnik):
        self.x  = x
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.m  = m
        self.r  = r
        self.color = color
        self.name = name
        self.sputnik = sputnik
    def draw_planet(self, name, screen, x_centre, y_centre, scale):
        if (self.sputnik == 0):
            label = font.render(self.name, True, "green")
            screen.blit(label, (x_centre + self.x*scale, y_centre + self.y*scale))
            draw.circle (screen, self.color, (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 10))
            draw.circle (screen, (200, 200, 200), (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 10), 1)
        elif (self.sputnik == 1) & (self.r * scale >= 1):
            label = font.render(self.name, True, "green")
            screen.blit(label, (x_centre + self.x*scale, y_centre + self.y*scale))
            draw.circle (screen, self.color, (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 6))
            draw.circle (screen, (200, 200, 200), (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 6), 1)
        else:
            draw.circle (screen, self.color, (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 2))
            draw.circle (screen, (200, 200, 200), (x_centre + self.x*scale, y_centre + self.y*scale), max(self.r*scale, 2), 1)
    @staticmethod
    def calc_en (planets):
        en_pot = 0
        en_kin = 0
        for planet in planets:
            en_kin += planet.m * (planet.vx**2 + planet.vy**2)
            for planet_i in planets:
                if planet_i is not planet:
                    en_pot -= Planet.G * planet_i.m * planet.m / ((planet.x - planet_i.x)**2 + (planet.y - planet_i.y)**2)**0.5
        return (en_pot + en_kin)*0.5

def movement(planets, itr, frame_skip, scale, x_centre, y_centre, en_min, en_max):
    for planet in planets:
        ax_pl = 0
        ay_pl = 0
        for planet_i in planets:
            if planet_i is not planet:
                common_factor = Planet.G * planet_i.m / ((planet.x - planet_i.x)**2 + (planet.y - planet_i.y)**2)**1.5
                ax_pl -= (planet.x - planet_i.x) * common_factor
                ay_pl -= (planet.y - planet_i.y) * common_factor
        
        planet.vx += ax_pl*dt
        planet.vy += ay_pl*dt
        planet.x  += planet.vx*dt
        planet.y  += planet.vy*dt
        if not (itr % frame_skip):
            planet.draw_planet(planet_i.name, screen, x_centre, y_centre, scale)
            pygame.display.update()
    if not (itr % frame_skip):
        screen.fill(SPACE_COLOR)
        en = Planet.calc_en(planets)
        en_min = min(en_min, en)
        en_max = max(en_max, en)
        #print("{0:d} {1:6.2f}    {2:+e}".format(itr*dt, timer.tick(), en/en_0-1))
    return(itr)
#параметры объектов сол. системы
M_sun = 1.989E30
M_earth = 5.972E24
M_moon = 7.35E22
R_sun = 6.964E8
R_earth = 6.371E6
R_moon = 1737100
color_sun = "yellow"
color_earth = "blue"
color_moon = "white"

#делаем планеты
sus    = Planet("sus",M_sun, R_sun, color_sun, x=0, y=0, vx=0, vy=0, sputnik = 0)
mogus   = Planet("mogus",M_earth, R_earth, color_earth, x=1.5E11, y=0, vx=0, vy=30000, sputnik = 0)
bobus   = Planet("bobus",M_moon, R_moon, color_moon, x=1.5E11 + 384400000, y=0, vx=0, vy=31000, sputnik = 1)

planets = [sus, mogus, bobus]
itr = 0
f = 100000
flag = 1

#шрифт для текста
font = pygame.font.Font('TlwgTypo.ttf', 25)

dt = 10
frame_skip = 86400//dt 
scale = 2E-9 #пикселей в метре

en_0 = Planet.calc_en(planets)
en_min = en_0
en_max = en_0

#параметры управления  визуализации
sensitivity = 0.05
x_centre = WIN_WIDTH / 2
y_centre = WIN_HEIGHT / 2
def distance(c1, c2):
    l = sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    return l
flag_planet_centre = 0

done = False
#основной цикл
while not done:
    for e in pygame.event.get():
        if e.type == QUIT:
            done = True
            break
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                scale *= (1 + sensitivity)
            elif e.button == 5:
                scale /= (1 + sensitivity)
            elif e.button == 1:
                print (mogus.x, mogus.y)
                x0, y0 = mouse.get_pos()
                for planet_i in planets:
                    print((x0 - x_centre) / scale, (y0 - y_centre) / scale, planet_i.x, planet_i.y)
                    if (distance(((x0 - x_centre) / scale, (y0 - y_centre) / scale), (planet_i.x, planet_i.y)) <= max(20 / scale , 2 * planet_i.r)):
                        flag_planet_centre = 1
                        planet_centre = planet_i
                        button_up = True
                        break;
                    else:
                        button_up = False
                        flag_planet_centre = 0 
                x_centre0 = x_centre
                y_centre0 = y_centre
                while not button_up:
                    x_now, y_now = mouse.get_pos()
                    x_centre = x_centre0 + x_now - x0
                    y_centre = y_centre0 + y_now - y0
                    movement(planets, itr, frame_skip, scale, x_centre, y_centre, en_min, en_max)
                    itr+=1
                    
                    for event_a in pygame.event.get():
                        if event_a.type == MOUSEBUTTONUP:
                            button_up = True
    if (flag_planet_centre == 1):
        x_centre = -planet_centre.x * scale + WIN_WIDTH/2
        y_centre = -planet_centre.y * scale + WIN_HEIGHT/2
        #print(x_centre, y_centre)
    movement(planets, itr, frame_skip, scale, x_centre, y_centre, en_min, en_max)
    
    itr+=1
    
print ("max deviations: {0:+e} to {1:+e}".format(en_min/en_0-1, en_max/en_0-1))

    
pygame.quit()

