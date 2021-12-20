from frame import *
import pygame as pg

def draw_bodies(bodies, surf, frame, drawlines = True):
    for body in bodies:
        for part in body.part:
            if drawlines:
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
            
def draw_pseudobody(part_set, vx, vy, surf, frame):
    for part in part_set:
        pg.draw.circle (surf, "0xD0D0D0", frame.direct((part.x, part.y)), round(part.r * frame.scale), 1)
    for part in part_set:
        pg.draw.circle(surf, part.color, frame.direct((part.x, part.y)), round(part.r * frame.scale - 1))
    if len(part_set):
        some_part = next(iter(part_set))
        part_screen_x, part_screen_y = frame.direct( (some_part.x, some_part.y) )
        part_screen_x_1, part_screen_y_1 = frame.direct( (some_part.x + vx, some_part.y + vy) )
        pg.draw.line (surf, "0x00D0D0", (part_screen_x, part_screen_y), (part_screen_x_1, part_screen_y_1))









































