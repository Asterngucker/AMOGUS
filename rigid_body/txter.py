"""
модуль содержит функции для чтения и записи в файл системы тел

функции:
    file_to_bodies(filename): -> (set, set)
    bodies_to_file(filename, set, set):
"""
from rigid import *

def file_to_bodies(filename):
    """
    создаёт и возвращает множества тел из текстового файла вида:
    l/m vx vy omeg      : лёгкое/массивное, скорость и угловая скорость. Остальные параметры вычисляются из параметров деталей тела. 
    {
    m r color x y       : масса, радиус детали, цвет, положение. Как мимнимум 1 деталь.
    ...       
    m r color x y       
    }
    
    **filename** — имя входного файла
    """
    massive_bodies = set()
    light_bodies = set()
    
    PARAMS = 2
    OPENNING = 3
    PARTS = 4
    state = PARAMS
    with open(filename) as f:
        for line in f:
            if len(line.strip()) != 0 and line[0] != '#':
                if state == PARAMS:
                    divided = line.split()
                    subset = divided[0]
                    vx   = float(divided[1])
                    vy   = float(divided[2])
                    omeg = float(divided[3])
                    state = OPENNING
                elif state == OPENNING:
                    part_set = set()
                    state = PARTS
                elif state == PARTS:
                    if line[0] != "}":
                        divided = line.split()
                        m      = float(divided[0])
                        r      = float(divided[1])
                        color  = divided[2]
                        x      = float(divided[3])
                        y      = float(divided[4])
                        part_set.add( Rigid_body.Part_circle(m=m, r=r, color=color, x=x, y=y) )
                    else:
                        body = Rigid_body(part_set, vx=vx, vy=vy, omeg=omeg)
                        if subset == "m":
                            massive_bodies.add(body)
                        elif subset == "l":
                            light_bodies.add(body)
                        state = PARAMS
                    
    return massive_bodies, light_bodies

def bodies_to_file(filename, massive_bodies, light_bodies):
    """Сохраняет данные о телах в файл
    формат совпадает с форматом функции-парсера

    **filename** — имя выходного файла
    **massive_bodies** — множество массивных тел
    **light_bodies** — множество лёгких тел
    """
    with open(filename, 'w') as f:
        f.write("#автосохранение\n\n")
        for body in massive_bodies | light_bodies:
            if body in massive_bodies:
                subset = "m"
            else:
                subset = "l" 
            f.write("{0:s} {1:+20.15E} {2:+20.15E} {3:+20.15E} \n".format(subset, body.vx, body.vy, body.omeg))
            f.write("{\n")
            for part in body.part:
                if not isinstance(part.color, str):  
                    part.color = hex(part.color[0] + 256*part.color[1] + 65536*part.color[2])
                f.write("{0:+20.15E} {1:+20.15E} {2:s} {3:+20.15E} {4:+20.15E}\n".format(part.m, part.r, part.color, part.x, part.y))
            f.write("}\n")
            f.write("\n")
