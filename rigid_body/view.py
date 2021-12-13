from frame import *
import pygame as pg

def draw_bodies(bodies, surf, frame):
    for body in bodies:
        for part in body.part:
            pg.draw.line (surf, "0x00D0D0", frame.direct((part.x, part.y)), frame.direct((body.x, body.y)) )
            pg.draw.circle (surf, "0xD0D0D0", frame.direct((part.x, part.y)), round(part.r * frame.scale), 1)
    for body in bodies:
        for part in body.part:
            pg.draw.circle(surf, part.color, frame.direct((part.x, part.y)), round(part.r * frame.scale - 1))
    for body in bodies:
        body_screen_x, body_screen_y = frame.direct((body.x, body.y))
        icon_size = 10
        if icon_size != 0:
            pg.draw.lines (surf, "0x00D0D0", True, [(body_screen_x, body_screen_y + icon_size), (body_screen_x + icon_size, body_screen_y), (body_screen_x, body_screen_y - icon_size), (body_screen_x - icon_size, body_screen_y)])
            #if body.name != "":
            #    pg.draw.lines (surf, "0x00D0D0", False, [(body_screen_x + icon_size/2, body_screen_y + icon_size/2), (body_screen_x + icon_size*2, body_screen_y + icon_size*2), (body_screen_x + icon_size*(6+2*len(body.name)), body_screen_y + icon_size*2)])
            

