class Tree_root:                           #вершина дерева Square_tree. Используется только в классе Square_tree
    def __init__ (root, parent, x, y, r):
        root.parent = parent     #родственные связи. Только у коренного элемента родитель None
        root.child_lu = None
        root.child_ru = None
        root.child_rd = None
        root.child_ld = None
        root.gas = set()         #множество частиц, перессекающихся с этим элементом. Все такие элементы полностью покрывают частицу.
        root.light = False       #наличие непустых gas в этом поддереве. Метод поиска столкновений get_intersect заходит в вершину только если в ней "горит свет"
        root.x = x  #координаты центра и полусторона
        root.y = y
        root.r = r
	
    def upd_light_up(root):  #обновление light в вершинах-предках. Останавливается, если light остался неизменным - при корректной работе это означает, что факт наличия элементов в этом поддереве не изменился.
        light_was = False
        light_is = True
        while root is not None and (light_was != light_is):
            light_was = root.light
            root.light = (len(root.gas)!=0) or (root.child_lu is not None and root.child_lu.light) or (root.child_ru is not None and root.child_ru.light) or (root.child_rd is not None and root.child_rd.light) or (root.child_ld is not None and root.child_ld.light)
            light_is = root.light
            root = root.parent
        
    def make_lca_up(root, box_x, box_y, box_r): #ищет минимальный элемент, покрывающий заданый и являющийся предком данного элемента. Нет необходимости отбрасывать последнее условие, т.к. это происходит в методе make_cover. В случае необходимости проращивает дерево наверх.
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
    
    def make_cover(root, box_x, box_y, box_r, elem, cover): #добавляет в множество cover элементы данного поддерева, пересекающиеся с данным квадратом и не меньшие его. Добавляет в множество gas выданную методу переменную. При необходимости проращивает дерево вглубь. Для корректной работы должна запускаться от вершины, полностью покрывающей данный эелемент.
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
    
    def get_intersect (root, intersect, gas_above): # добавляет в intersect пары потенциально пересекающихся элементов. Такими считаются те, чьё покрытие элемментами геометрически пересекается.
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

class Square_tree: #класс предоставляет интерфейс для поиска потенциально пересекающихся обьектов, вписанных в квадрат, называемый box.
    def __init__ (tree, x=1.0, y=1.0, r=1.0):
        tree.cover = dict()
        tree.root = Tree_root(None, x, y, r)
    
    def add_elem(tree, box_x, box_y, box_r, elem): #добавление элемента происходит путём "обманывания" метода upd_elem - делаем вид что данный обьект раньше был покрыт корнем дерева и просим обновить его данные в дереве.
        tree.cover[elem] = {tree.root}
        tree.root.gas.add(elem)
        tree.upd_elem(box_x, box_y, box_r, elem)
    
    def upd_elem(tree, box_x, box_y, box_r, elem): #обновление покрытия данного обьекта с данной габаритной коробкой - квадратом с центром box_x, box_y и полустороной box_r.
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
        for root in old_cover - new_cover:
            root.gas.remove(elem)
            root.upd_light_up()
        for root in new_cover - old_cover:
            root.gas.add(elem)
            root.upd_light_up()
        
        tree.cover[elem] = new_cover
    
    def del_elem(tree, elem): #удаляемый элемент должен присутствовать в дереве
        for root in tree.cover[elem]:
            root.gas.remove(elem)
            root.upd_light_up()
        del tree.cover[elem]
    
    def get_intersect(tree): #возвращает множество пар потенциально пересекающихся элементов
        intersect = set()
        gas_above = set()
        tree.root.get_intersect(intersect, gas_above)
        return intersect
    
