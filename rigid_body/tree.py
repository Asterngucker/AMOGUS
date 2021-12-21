"""
Модуль для более эффективного обнаружения столкновений

Классы:
    Tree_root
    Square_tree
"""

class Tree_root:
    """
    вершина дерева в структуре данных для определение потециально пересекающихся объектов.
    Этот класс не предназначен для прямого использования, см. класс Square_tree
    
    Атрибуты:
    ---------
    parent: Tree_root
        родительская вершина
    child_lu: Tree_root
         верхний-левый потомок
    child_ru: Tree_root
        верхний-правый потомок
    child_rd: Tree_root
        нижний-правый потомок
    child_ld: Tree_root
        нижний-левый потомок
    gas: set 
        множество объектов, для которых эта вершина является частью покрытия
    light: bool
         непустота данного поддерева
    x: float
        x цетра вершины
    y: float
        y цетра вершины
    r: float
        полусторона вершины
        
    Методы:
    -------
    upd_light_up ():
        обновляет light вершинах-предках.
    make_lca_up (box_x: float, box_y: float, box_r: float):
        начиная с  данной вершины ищет минимальную вершину, полностью покрывающую данный квадрат box
    make_cover(box_x: float, box_y: float, box_r: float, elem, cover: set):
        Определяет порытие данного элемента. Добавляет в вершины покрытия элемент, добавляет в cover эти вершины.
    get_intersect (intersect: set, gas_above: set):
        в множество intersect записывает пары потенциально пересекающихся элементов. gas_above следует инициализировать пустым
    trunc_empty():
        обрезает пустые поддеревья, предоставляя их сборщику мусора
    """
    def __init__ (root, parent, x, y, r):
        root.parent = parent
        root.child_lu = None
        root.child_ru = None
        root.child_rd = None
        root.child_ld = None
        root.gas = set()
        root.light = False
        root.x = x
        root.y = y
        root.r = r
	
    def upd_light_up(root):
        light_was = False
        light_is = True
        while root is not None and (light_was != light_is):
            light_was = root.light
            root.light = (len(root.gas)!=0) or (root.child_lu is not None and root.child_lu.light) or (root.child_ru is not None and root.child_ru.light) or (root.child_rd is not None and root.child_rd.light) or (root.child_ld is not None and root.child_ld.light)
            light_is = root.light
            root = root.parent
        
    def make_lca_up(root, box_x, box_y, box_r):
        while box_x-root.x-box_r<-root.r or box_y-root.y-box_r<-root.r or box_x-root.x+box_r>root.r or box_y-root.y+box_r>root.r:
            if root.parent is None:
                if   box_x>root.x and box_y>root.y:
                    root.parent = Tree_root(None, root.x+root.r, root.y+root.r, root.r*2)
                    root.parent.child_lu = root
                elif box_x<root.x and box_y>root.y:
                    root.parent = Tree_root(None, root.x-root.r, root.y+root.r, root.r*2)
                    root.parent.child_ru = root
                elif box_x<root.x and box_y<root.y:
                    root.parent = Tree_root(None, root.x-root.r, root.y-root.r, root.r*2)
                    root.parent.child_rd = root
                else:
                    root.parent = Tree_root(None, root.x+root.r, root.y-root.r, root.r*2)
                    root.parent.child_ld = root
            root = root.parent
        return root
    
    def make_cover(root, box_x, box_y, box_r, elem, cover): 
        if root.r<box_r*2:
            root.gas.add(elem)
            cover.add(root)
        else:
            if box_x-root.x<box_r and box_y-root.y<box_r:
                if root.child_lu is None:
                    root.child_lu = Tree_root(root, root.x-root.r/2, root.y-root.r/2, root.r/2)
                root.child_lu.make_cover(box_x, box_y, box_r, elem, cover)
            
            if box_x-root.x>-box_r and box_y-root.y<box_r:
                if root.child_ru is None:
                    root.child_ru = Tree_root(root, root.x+root.r/2, root.y-root.r/2, root.r/2)
                root.child_ru.make_cover(box_x, box_y, box_r, elem, cover)
            
            if box_x-root.x>-box_r and box_y-root.y>-box_r:
                if root.child_rd is None:
                    root.child_rd = Tree_root(root, root.x+root.r/2, root.y+root.r/2, root.r/2)
                root.child_rd.make_cover(box_x, box_y, box_r, elem, cover)
            
            if box_x-root.x<box_r and box_y-root.y>-box_r:
                if root.child_ld is None:
                    root.child_ld = Tree_root(root, root.x-root.r/2, root.y+root.r/2, root.r/2)
                root.child_ld.make_cover(box_x, box_y, box_r, elem, cover)
    
    def get_intersect (root, intersect, gas_above):
        gas_this_and_above = gas_above | root.gas
        for elem_1 in root.gas:
            for elem_2 in gas_this_and_above:
                if elem_1 is not elem_2 and (elem_2, elem_1) not in intersect:
                    intersect.add((elem_1, elem_2))
        if root.child_lu is not None and root.child_lu.light:
            root.child_lu.get_intersect(intersect, gas_this_and_above)
        if root.child_ru is not None and root.child_ru.light:
            root.child_ru.get_intersect(intersect, gas_this_and_above)
        if root.child_rd is not None and root.child_rd.light:
            root.child_rd.get_intersect(intersect, gas_this_and_above)
        if root.child_ld is not None and root.child_ld.light:
            root.child_ld.get_intersect(intersect, gas_this_and_above)
    
    def trunc_empty (root):
        if root.child_lu is not None: 
            if not root.child_lu.light:
                root.child_lu = None
            else:
                root.child_lu.trunc_empty()
        
        if root.child_ru is not None: 
            if not root.child_ru.light:
                root.child_ru = None
            else:
                root.child_ru.trunc_empty()
        
        if root.child_rd is not None: 
            if not root.child_rd.light:
                root.child_rd = None
            else:
                root.child_rd.trunc_empty()
        
        if root.child_ld is not None: 
            if not root.child_ld.light:
                root.child_ld = None
            else:
                root.child_ld.trunc_empty()
    
class Square_tree:
    """
    Класс служит для эффективного обнаружения столкновений.
    
    Атрибуты:
    ---------
    cover: dict
        каждому поддерживаемому объекту сопоставлено множество вершин, полностью покрывающих его
    root: Tree_root
        корень дерева
    
    Методы:
    -------
    add_elem(float, float, float, object):
        добавление объекта в дерево.
    upd_elem(float, float, float, object):
        обновление положения объекта
    del_elem(object):
        удаление объекта
    get_intersect(): -> set
        определение потенциально пересекающихся объектов
    trunc_empty():
        удаление пустых поддеревьев.
    """
    def __init__ (tree, x=1.0, y=1.0, r=1.0):
        tree.cover = dict()
        tree.root = Tree_root(None, x, y, r)
    
    def add_elem(tree, box_x, box_y, box_r, elem):
        """
        Добавление нового объекта в дерево.
        
        **box_x** — координата x центра ограничивающего квадрата
        **box_y** — координата y центра ограничивающего квадрата
        **box_r** — полусторона ограничивающего квадрата
        **elem** — объект произвольного класса, будет возвращен как элемент пары методом get_intersect
        """
        if elem not in tree.cover:
            tree.cover[elem] = {tree.root}
            tree.root.gas.add(elem)
        tree.upd_elem(box_x, box_y, box_r, elem)
    
    def upd_elem(tree, box_x, box_y, box_r, elem):
        """
        Обновление полложения объекта в дереве.
        
        **box_x** — координата x центра ограничивающего квадрата
        **box_y** — координата y центра ограничивающего квадрата
        **box_r** — полусторона ограничивающего квадрата
        **elem** — обновляемый объект
        """
        #поиск вершины, полностью покрывающей данную коробку. Запускается из случайной вершины прежнего покрытия, тк подразумевается что перемещение за итерацию невелико
        lca = next(iter(tree.cover[elem]))
        lca = lca.make_lca_up(box_x, box_y, box_r)
        while tree.root.parent is not None:
            tree.root.upd_light_up()
            tree.root = tree.root.parent
        #поиск нового покрытия
        new_cover = set()
        lca.make_cover(box_x, box_y, box_r, elem, new_cover)
        old_cover = tree.cover[elem]
        #обноввление множеств покрываемых элементов в вершинах дерева.
        for root in new_cover - old_cover:
            root.gas.add(elem)
            root.upd_light_up()
        for root in old_cover - new_cover:
            root.gas.remove(elem)
            root.upd_light_up()
        
        tree.cover[elem] = new_cover
    
    def del_elem(tree, elem):
        """
        удаление объекта из дерева
        
        **elem** — обновляемый объект
        """
        for root in tree.cover[elem]:
            root.gas.remove(elem)
            root.upd_light_up()
        del tree.cover[elem]
    
    def get_intersect(tree):
        """
        возвращает множество пар потенциально пересекающихся элементов
        """
        intersect = set()
        gas_above = set()
        tree.root.get_intersect(intersect, gas_above)
        return intersect
    
    def trunc_empty(tree):
        """
        обрезает пустые ветки дерева
        """
        tree.root.trunc_empty()
