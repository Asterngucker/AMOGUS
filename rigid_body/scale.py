from math import *

class Frame:
    '''
    Класс для перехода между системами ортонормированных координат.
    Объект класса хранит масштаб, угол и пололжение начала координат данной системы координат в исходной. 
    Также хранится переменная flip_y в связи с инверсией оси y в общепринятой экранной системе координат
    Методы класса предназначены для перевода значений координат и обновления переменных объекта класса.
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
    
    @alph.setter
    def alph(frame, alph):
        frame._alph = alph
        frame.sin_alph = sin(alph)
        frame.cos_alph = cos(alph)
    
    def direct(frame, pos): #pos - пара координат x y. Возвращает пару координат после преобразования.
        if not frame.flip_y:
            return frame.x_0 + frame.scale*(frame.cos_alph*pos[0] - frame.sin_alph*pos[1]), frame.y_0 + frame.scale*(frame.sin_alph*pos[0] + frame.cos_alph*pos[1])
        else:
            return frame.x_0 + frame.scale*(frame.cos_alph*pos[0] + frame.sin_alph*pos[1]), frame.y_0 + frame.scale*(frame.sin_alph*pos[0] - frame.cos_alph*pos[1])
    
    def inverse(frame, pos): #Обратное преобразование
        if not frame.flip_y:
            return 1/frame.scale*(frame.cos_alph*(pos[0]-frame.x_0) + frame.sin_alph*(pos[1]-frame.y_0)), 1/frame.scale*(-frame.sin_alph*(pos[0]-frame.x_0) + frame.cos_alph*(pos[1]-frame.y_0))
        else:
            return 1/frame.scale*(frame.cos_alph*(pos[0]-frame.x_0) + frame.sin_alph*(pos[1]-frame.y_0)), 1/frame.scale*(-frame.sin_alph*(pos[0]-frame.x_0) + frame.cos_alph*(pos[1]-frame.y_0))
    
    def drag (frame, delta_pos): #для перетаскивания курсором. delta_pos - изменение положения курсора в экранных коор-ах или привязки к объекту.
        frame.x_0 += delta_pos[0]
        frame.y_0 += delta_pos[1]
    
    def scale_at_point (frame, pos, factor): #увеличивает масштаб в factor раз, оставляя данную экранную точку pos == (x, y) на месте. Для масштабирования курсором.
        frame.x_0 += (1 - factor) * (pos[0] - frame.x_0)
        frame.y_0 += (1 - factor) * (pos[1] - frame.y_0)
        frame.scale *= factor
        
