from math import *
"""
модуь содержит класс для работы с системами координат

Класс:
    Frame
"""
class Frame:
    '''
    Класс для перехода между системами ортонормированных координат.
    Объект класса хранит масштаб, угол и пололжение начала координат данной системы координат в исходной. 
    Также хранится переменная flip_y в связи с инверсией оси y в общепринятой экранной системе координат
    Методы класса предназначены для перевода значений координат и обновления переменных объекта класса.
    
    атрибуты:
    ---------
    x_0: float
        положение по x начала координат старой системы отсчёта отн. новой
    y_0: float
        положение по y начала координат старой системы отсчёта отн. новой
    scale: float
        масштаб
    _alph: 
        угол поворота 
    flip_y:
        перевернута ли ось y в новой СО отн. старой
    sin_alph: float
        синус угла. Хранится чтобы не пересчитывать его каждый раз
    cos_alph: float
        косинус угла. Хранится чтобы не пересчитывать его каждый раз
    
    методы:
        direct(pos: (float, float)): -> (float, float)
            прямое преобразование
        inverse(pos: (float, float)): -> (float, float)
            обратное преобразование
        drag(delta_pos: (float, float)):
            изменение положения начала координат
        scale_at_point (pos: (float, float), factor: float):
            масштабирование, оставляющее выбраную точку на месте
        rotate_around (pos: (float, float), alph: float):
            поворот вокруг данной точки
    '''
    def __init__ (frame):
        frame.x_0 = 0
        frame.y_0 = 0
        frame.scale = 1
        frame._alph = 0      #вместе с углом должны меняться и sin, cos угла.
        frame.flip_y = False
        
        frame.sin_alph = 0.0 #сопутствующие переменные, обновляемые при изменении угла.
        frame.cos_alph = 1.0
    
    @property
    def alph(frame):
        return frame._alph
        
    @alph.getter
    def alph(frame, alph):
        return frame._alph
    
    @alph.setter
    def alph(frame, alph):
        frame._alph = alph
        frame.sin_alph = sin(alph)
        frame.cos_alph = cos(alph)
    
    def direct(frame, pos):
        """
        Возвращает пару координат после преобразования
        
        **pos**  - пара координат x y.
        """
        if not frame.flip_y:
            return frame.x_0 + frame.scale*(frame.cos_alph*pos[0] - frame.sin_alph*pos[1]), frame.y_0 + frame.scale*(frame.sin_alph*pos[0] + frame.cos_alph*pos[1])
        else:
            return frame.x_0 + frame.scale*(frame.cos_alph*pos[0] + frame.sin_alph*pos[1]), frame.y_0 + frame.scale*(frame.sin_alph*pos[0] - frame.cos_alph*pos[1])
    
    def inverse(frame, pos):
        """
        Возвращает пару координат после обратного преобразования
        
        **pos**  - пара координат x y.
        """
        if not frame.flip_y:
            return 1/frame.scale*(frame.cos_alph*(pos[0]-frame.x_0) + frame.sin_alph*(pos[1]-frame.y_0)), 1/frame.scale*(-frame.sin_alph*(pos[0]-frame.x_0) + frame.cos_alph*(pos[1]-frame.y_0))
        else:
            return 1/frame.scale*(frame.cos_alph*(pos[0]-frame.x_0) + frame.sin_alph*(pos[1]-frame.y_0)), 1/frame.scale*( frame.sin_alph*(pos[0]-frame.x_0) - frame.cos_alph*(pos[1]-frame.y_0))
    
    def drag (frame, delta_pos):
        """
        меняет начало координат
        
        **delta_pos** - смещение по x и y.
        """
        frame.x_0 += delta_pos[0]
        frame.y_0 += delta_pos[1]
    
    def scale_at_point (frame, pos, factor):
        """
        увеличивает масштаб в factor раз, оставляя данную экранную точку pos на месте.
        
        **pos**  - пара координат x y.
        **factor** - увеличение масштаба
        """
        frame.x_0 += (1 - factor) * (pos[0] - frame.x_0)
        frame.y_0 += (1 - factor) * (pos[1] - frame.y_0)
        frame.scale *= factor
    
    def rotate_around(frame, pos, alph):
        """
        поворот вокруг данной точки
        
        **pos**  - пара координат x y.
        **alph** - угол поворота
        """
        frame.alph = frame._alph + alph
        cos_alph = cos(alph)
        sin_alph = sin(alph)
        frame.x_0, frame.y_0 = pos[0] - (cos_alph*(pos[0]-frame.x_0) - sin_alph*(pos[1]-frame.y_0)), pos[1] - (sin_alph*(pos[0]-frame.x_0) + cos_alph*(pos[1]-frame.y_0))
