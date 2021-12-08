import pygame as pg
import math

class Rigid_body:
    class Part_circle:
        def __init__ (part, m=1, r=10, color=(0, 0, 0), x=0, y=0, body = None):
            part.m = m
            part.r = r
            part.color = color
            part.x = x
            part.y = y
            
            part.x_local = 0
            part.y_local = 0
            part.body = None
    
    def __init__ (body, part_set, vx=0, vy=0, omeg=0):
        body.vx = vx
        body.vy = vy
        body.omeg = omeg
        body.part = part_set
        
        m_x = 0
        m_y = 0
        m_tot = 0
        j = 0
        for part in part_set:
            m_x += part.x*part.m
            m_y += part.y*part.m
            m_tot += part.m
            j += (part.x**2 + part.y**2 + 0.5*part.r**2)*part.m
            
        body.x = m_x/m_tot
        body.y = m_y/m_tot
        body.alph = 0
        body.m = m_tot
        body.j = j - (body.x**2 + body.y**2) * body.m
        
        for part in part_set:
            part.body = body
            part.x_local = part.x - body.x
            part.y_local = part.y - body.y
    
    def add_part (body, part):
        pass
    
    def del_part (body, part):
        pass
    
    def merge_body (body_1, body_2):
        pass
    
    def calc_coll(part_1, part_2):
        if (part_1.x - part_2.x)**2 + (part_1.y - part_2.y)**2 < (part_1.r + part_2.r)**2:
            body_1 = part_1.body
            body_2 = part_2.body
            vx_1 = body_1.vx - body_1.omeg * (part_1.y - body_1.y)
            vy_1 = body_1.vy + body_1.omeg * (part_1.x - body_1.x)
            vx_2 = body_2.vx - body_2.omeg * (part_2.y - body_2.y)
            vy_2 = body_2.vy + body_2.omeg * (part_2.x - body_2.x)
            a_x = part_2.x - part_1.x
            a_y = part_2.y - part_1.y
            if (vx_2-vx_1)*a_x + (vy_2-vy_1)*a_y < 0:
                a_sqr = a_x**2 + a_y**2
                r1_x = part_1.x - body_1.x
                r1_y = part_1.y - body_1.y
                r2_x = part_2.x - body_2.x
                r2_y = part_2.y - body_2.y
                
                mu_1 = body_1.m * body_1.j / (body_1.j + body_1.m * (r1_y*a_x - r1_x*a_y)**2 / a_sqr)
                mu_2 = body_2.m * body_2.j / (body_2.j + body_2.m * (r2_y*a_x - r2_x*a_y)**2 / a_sqr)
                momentum_div_a = -2.0 * mu_1*mu_2/(mu_1 + mu_2) * ((vx_1-vx_2)*a_x + (vy_1-vy_2)*a_y)/a_sqr
                momentum_x = momentum_div_a * a_x
                momentum_y = momentum_div_a * a_y
                
                body_1.vx   += momentum_x / body_1.m
                body_1.vy   += momentum_y / body_1.m
                body_1.omeg += (momentum_y*r1_x - momentum_x*r1_y) / body_1.j
                body_2.vx   -= momentum_x / body_2.m
                body_2.vy   -= momentum_y / body_2.m
                body_2.omeg -= (momentum_y*r2_x - momentum_x*r2_y) / body_2.j
                
    def move_dt(body, dt, g=0):
        body.x+= body.vx*dt
        body.y+= body.vy*dt - 0.5*g*dt**2
        body.alph += body.omeg * dt
        
        sin_alph = math.sin(body.alph)
        cos_alph = math.cos(body.alph)
        for part in body.part:
            part.x = body.x + part.x_local*cos_alph - part.y_local*sin_alph
            part.y = body.y + part.x_local*sin_alph + part.y_local*cos_alph
        body.vy-= g*dt
    
    def draw_body(body, surf):
        for part in body.part:
            pg.draw.line (surf, (0, 200, 200), (part.x, part.y), (body.x, body.y))
        for part in body.part:
            pg.draw.circle(surf, (200, 200, 200), (part.x, part.y), part.r, 1)
        for part in body.part:
            pg.draw.circle(surf, part.color, (part.x, part.y), part.r - 1)
           
