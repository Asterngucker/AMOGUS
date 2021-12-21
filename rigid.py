"""
Модуль содержит класс Rigid_body
"""
from math import *


class Rigid_body:
    """
    Класс описыват твердое тело, состоящее из деталей-сфер

    атрибуты:
    ---------
    m: float
        масса тела. Сумма масс деталей
    j: float
        моммент инерции тела. Вычисляется по Т. Гюйгенса-Штейнера
    x: float
        координата центра масс по оси x
    y: float
        координата центра масс по оси y
    alph: float
        угловая координата
    vx: float
        скорость по x
    vy: float
        скорость по y
    omeg: float
        угловая скорость
    part: set
        множество деталей
    
    методы:
    -------
    copy(): -> body
        возвращает капию тела
    calc_coll(part_1: Part_circle, part_2: Part_circle):
        расчет упругого столкновения 2 тел
    calc_coll_massive(part: Part_circle, part_massive: Part_circle):
        упругое столкновение с телом много большей массы
    runge_kutta_n_body(massive_bodies: set, all_bodies: set, time_step: float):
        метод Рунге-Кутты для итерации движения
    calc_energy(massive_bodies: set, all_bodies: set, time_step: float): -> float
        расчёт энергии системы
    """
    G = 6.67E-11

    class Part_circle:
        """
        вспомогательныый класс для хранения атрибутов детали

        атрибуты:
        ---------
        m: float
            масса детали
        r: float
            радиус детали
        color: float
            цвет
        x: float
            координата x в мировой СО
        y: float
            координата y в мировой СО
        x_local: float
            координата x в СО самого тела
        y_local: float
            координата y в СО самого тела
        body: Rigid_body
            тело, чьей деталью является
        """
        def __init__(part, m=1, r=10, color=(0, 0, 0), x=0, y=0, body=None):
            part.m = m
            part.r = r
            part.color = color
            part.x = x
            part.y = y

            part.x_local = 0
            part.y_local = 0
            part.body = None

    def __init__(body, part_set, vx=0, vy=0, omeg=0):
        body.vx = vx
        body.vy = vy
        body.omeg = omeg
        body.part = part_set

        m_x = 0
        m_y = 0
        m_tot = 0
        j = 0
        for part in part_set:
            m_x += part.x * part.m
            m_y += part.y * part.m
            m_tot += part.m
            # учитывается момент инерции детали-сферы.
            j += (part.x**2 + part.y**2 + 0.4 * part.r**2) * part.m

        body.x = m_x / m_tot
        body.y = m_y / m_tot
        body.alph = 0
        body.m = m_tot
        body.j = j - (body.x**2 + body.y**2) * body.m

        for part in part_set:
            part.body = body
            part.x_local = part.x - body.x
            part.y_local = part.y - body.y

    def copy(body):
        """
        Возвращает копию данного тела
        """
        new_part_set = set()
        for part in body.part:
            new_part_set.add(
                Rigid_body.Part_circle(
                    m=part.m,
                    r=part.r,
                    color=part.color,
                    x=part.x,
                    y=part.y))
        new_body = Rigid_body(
            new_part_set,
            vx=body.vx,
            vy=body.vy,
            omeg=body.omeg)
        return new_body

    def merge_body(body_1, body_2):
        pass

    def calc_coll(part_1, part_2):
        """
        Упругое и гладкое столкновение 2 тел, заданное столкнувшимися деталями.
        Включает проверку на идентичность, пересечение и сближение.
        Импульс передаётся через линию соединяющую центры шаров-деталей.

        **part_1** — деталь 1 тела
        **part_2** — деталь 2 тела
        """
        body_1 = part_1.body
        body_2 = part_2.body
        if body_1 is not body_2 and (
                part_1.x - part_2.x)**2 + (part_1.y - part_2.y)**2 < (part_1.r + part_2.r)**2:
            vx_1 = body_1.vx - body_1.omeg * (part_1.y - body_1.y)
            vy_1 = body_1.vy + body_1.omeg * (part_1.x - body_1.x)
            vx_2 = body_2.vx - body_2.omeg * (part_2.y - body_2.y)
            vy_2 = body_2.vy + body_2.omeg * (part_2.x - body_2.x)
            a_x = part_2.x - part_1.x
            a_y = part_2.y - part_1.y
            if (vx_2 - vx_1) * a_x + (vy_2 - vy_1) * a_y < 0:
                a_sqr = a_x**2 + a_y**2
                r1_x = part_1.x - body_1.x
                r1_y = part_1.y - body_1.y
                r2_x = part_2.x - body_2.x
                r2_y = part_2.y - body_2.y

                mu_1 = body_1.m * body_1.j / \
                    (body_1.j + body_1.m * (r1_y * a_x - r1_x * a_y)**2 / a_sqr)
                mu_2 = body_2.m * body_2.j / \
                    (body_2.j + body_2.m * (r2_y * a_x - r2_x * a_y)**2 / a_sqr)
                momentum_div_a = -2.0 * mu_1 * mu_2 / \
                    (mu_1 + mu_2) * ((vx_1 - vx_2) * a_x + (vy_1 - vy_2) * a_y) / a_sqr
                momentum_x = momentum_div_a * a_x
                momentum_y = momentum_div_a * a_y

                body_1.vx += momentum_x / body_1.m
                body_1.vy += momentum_y / body_1.m
                body_1.omeg += (momentum_y * r1_x -
                                momentum_x * r1_y) / body_1.j
                body_2.vx -= momentum_x / body_2.m
                body_2.vy -= momentum_y / body_2.m
                body_2.omeg -= (momentum_y * r2_x -
                                momentum_x * r2_y) / body_2.j

    def calc_coll_massive(part, part_massive):
        """
        Упругое и гладкое столкновение 2, заданное столкнувшимися деталями.
        Включает проверку на идентичность, пересечение и сближение.
        Импульс передаётся через линию соединяющую центры шаров-деталей.

        **part** — деталь лёгкого тела
        **part_massive** — деталь тяжелого тела. Его траектория не изменится в результате удара
        """
        part_1 = part
        part_2 = part_massive
        body_1 = part_1.body
        body_2 = part_2.body
        if body_1 is not body_2 and (
                part_1.x - part_2.x)**2 + (part_1.y - part_2.y)**2 < (part_1.r + part_2.r)**2:
            vx_1 = body_1.vx - body_1.omeg * (part_1.y - body_1.y)
            vy_1 = body_1.vy + body_1.omeg * (part_1.x - body_1.x)
            vx_2 = body_2.vx - body_2.omeg * (part_2.y - body_2.y)
            vy_2 = body_2.vy + body_2.omeg * (part_2.x - body_2.x)
            a_x = part_2.x - part_1.x
            a_y = part_2.y - part_1.y
            if (vx_2 - vx_1) * a_x + (vy_2 - vy_1) * a_y < 0:
                a_sqr = a_x**2 + a_y**2
                r1_x = part_1.x - body_1.x
                r1_y = part_1.y - body_1.y
                r2_x = part_2.x - body_2.x
                r2_y = part_2.y - body_2.y

                mu_1 = body_1.m * body_1.j / (body_1.j + body_1.m * (r1_y * a_x - r1_x * a_y)**2 / a_sqr)
                momentum_div_a = -2.0 * mu_1 * ((vx_1 - vx_2) * a_x + (vy_1 - vy_2) * a_y) / a_sqr
                momentum_x = momentum_div_a * a_x
                momentum_y = momentum_div_a * a_y

                body_1.vx += momentum_x / body_1.m
                body_1.vy += momentum_y / body_1.m
                body_1.omeg += (momentum_y * r1_x - momentum_x * r1_y) / body_1.j

    def refresh_redundant(body):
        sin_alph = sin(body.alph)
        cos_alph = cos(body.alph)
        for part in body.part:
            part.x = body.x + part.x_local * cos_alph - part.y_local * sin_alph
            part.y = body.y + part.x_local * sin_alph + part.y_local * cos_alph

    class Motion_derivative:
        def __init__(k):
            k.x = dict()
            k.y = dict()
            k.alph = dict()
            k.vx = dict()
            k.vy = dict()
            k.omeg = dict()

    def apply_derivative(body, der, dt):
        body.x += dt * der.x[body]
        body.y += dt * der.y[body]
        body.alph += dt * der.alph[body]
        body.vx += dt * der.vx[body]
        body.vy += dt * der.vy[body]
        body.omeg += dt * der.omeg[body]

    # вычисляет производные параметров твёрдых тел при гравитационном
    # взаимодействии
    def get_grav_derivative(massive_bodies, all_bodies):
        G = 6.67E-11
        k = Rigid_body.Motion_derivative()
        for body in all_bodies:
            k.x[body] = body.vx
            k.y[body] = body.vy
            k.alph[body] = body.omeg
            k.vx[body] = 0
            k.vy[body] = 0
            k.omeg[body] = 0
            for grav_body in massive_bodies:
                if grav_body is not body:
                    for part in body.part:
                        for grav_part in grav_body.part:
                            delta_x = grav_part.x - part.x
                            delta_y = grav_part.y - part.y

                            # рассчёт силы взаимодействия 2 сфер по осям.
                            f_div_r = G * grav_part.m * part.m / ((delta_x)**2 + (delta_y)**2)**1.5
                            f_x = f_div_r * delta_x
                            f_y = f_div_r * delta_y

                            k.vx[body] += f_x
                            k.vy[body] += f_y
                            # момент сил, действующий на всё тело
                            k.omeg[body] += ((part.x - body.x) * f_y - (part.y - body.y) * f_x)
            # получаем производные скорости и угловой скорости
            k.vx[body] /= body.m
            k.vy[body] /= body.m
            k.omeg[body] /= body.j
        return k

    @staticmethod
    def runge_kutta_n_body(massive_bodies, all_bodies, time_step):
        """
        классичесский метод Рунге - Кутты для системы из лёгких и тяжёлых (создающих грав. поле) твёрдых тел, составленых из сфер.

        **massive_bodies** — множество тяжелых тел, создающих грав. поле
        **all_bodies** — множество всех тел
        **timestep** — дискретизация по времени
        """
        h = time_step  # в литературе шаг по времени обычно обозначают h

        k1 = Rigid_body.get_grav_derivative(massive_bodies, all_bodies)

        for body in all_bodies:  # переместим все тела для рассчёта следующего шага
            body.apply_derivative(k1, h / 2)
            body.refresh_redundant()
        k2 = Rigid_body.get_grav_derivative(massive_bodies, all_bodies)
        for body in all_bodies:
            body.apply_derivative(k1, -h / 2)  # переместим тела обратно
            # снова перемещаем, для третьего шага
            body.apply_derivative(k2, h / 2)
            body.refresh_redundant()
        k3 = Rigid_body.get_grav_derivative(massive_bodies, all_bodies)
        for body in all_bodies:
            body.apply_derivative(k2, -h / 2)
            body.apply_derivative(k3, h)
            body.refresh_redundant()
        k4 = Rigid_body.get_grav_derivative(massive_bodies, all_bodies)
        for body in all_bodies:
            body.apply_derivative(k3, -h)

        for body in all_bodies:
            body.apply_derivative(k1, h * 1 / 6)
            body.apply_derivative(k2, h * 2 / 6)
            body.apply_derivative(k3, h * 2 / 6)
            body.apply_derivative(k4, h * 1 / 6)
            body.refresh_redundant()

    @staticmethod
    def calc_energy(massive_bodies, all_bodies):
        """
        Возвращает полную механическую энергию системы тел

        **massive_bodies** — множество тяжелых тел, создающих грав. поле
        **all_bodies** — множество всех тел
        """
        en = 0
        for body in all_bodies:
            en += body.m * (body.vx**2 + body.vy**2) * 0.5 + body.j * body.omeg**2 / 2
            for body_1 in massive_bodies:
                if body is not body_1:
                    for part in body.part:
                        for part_1 in body_1.part:
                            en -= 0.5 * Rigid_body.G * (part.m * part_1.m) / ((part.x - part_1.x)**2 + (part.y - part_1.y)**2)**0.5
        return en
