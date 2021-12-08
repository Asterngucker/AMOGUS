import pygame as pg

def coor_to_screen(x, y, x_screen_0, y_screen_0, scale):
    return round(x_screen_0+scale*x), round(y_screen_0-scale*y)
    
def coor_to_model(x, y, x_screen_0, y_screen_0, scale):
    return (x_screen_0+scale*x), (y_screen_0-scale*y)

def drag_screen (delta_x_screen, delta_y_screen, x_screen_0, y_screen_0, scale):
    return x_screen_0 + delta_x_screen, y_screen_0 + delta_y_screen

def scale_at_point (x_screen, y_screen, scale_new, x_screen_0, y_screen_0, scale):
    return x_screen_0 + (1 - scale_new/scale) * (x_screen-x_screen_0), y_screen_0 + (1 - scale_new/scale) * (y_screen-y_screen_0)

def draw_root (root, screen, x_screen_0, y_screen_0, scale):
    if root.light:# or True:
        root_x_screen, root_y_screen = coor_to_screen(root.x, root.y, x_screen_0, y_screen_0, scale)
        root_r_screen  = root.r * scale
        if len(root.gas)!=0:
            pg.draw.rect (screen, (40, 130, 200), (root_x_screen-root_r_screen, root_y_screen-root_r_screen, 2*root_r_screen, 2*root_r_screen))
        pg.draw.rect (screen, (200, 200, 200), (root_x_screen-root_r_screen, root_y_screen-root_r_screen, 2*root_r_screen, 2*root_r_screen), 1)
        if root.child_lu is not None:
            draw_root(root.child_lu, screen, x_screen_0, y_screen_0, scale)
        if root.child_ru is not None:
            draw_root(root.child_ru, screen, x_screen_0, y_screen_0, scale)
        if root.child_rd is not None:
            draw_root(root.child_rd, screen, x_screen_0, y_screen_0, scale)
        if root.child_ld is not None:
            draw_root(root.child_ld, screen, x_screen_0, y_screen_0, scale)

def draw_body(body, surf, x_screen_0, y_screen_0, scale):
    for part in body.part:
        part_x_screen, part_y_screen = coor_to_screen(part.x, part.y, x_screen_0, y_screen_0, scale)
        body_x_screen, body_y_screen = coor_to_screen(body.x, body.y, x_screen_0, y_screen_0, scale)
        pg.draw.line (surf, (0, 200, 200), (part_x_screen, part_y_screen), (body_x_screen, body_y_screen))
    for part in body.part:
        part_x_screen, part_y_screen = coor_to_screen(part.x, part.y, x_screen_0, y_screen_0, scale)
        pg.draw.circle(surf, (200, 200, 200), (part_x_screen, part_y_screen), round(part.r * scale), 1)
    for part in body.part:
        part_x_screen, part_y_screen = coor_to_screen(part.x, part.y, x_screen_0, y_screen_0, scale)
        pg.draw.circle(surf, part.color, (part_x_screen, part_y_screen), round(part.r * scale - 1))
            
