from math import sqrt

from kivy.core.window import Window
from kivy.uix.widget import Widget

from input import tree

def chunk(group, chunk_size):
    chunk_list = []
    for i in range(0, len(group), chunk_size):
        chunk_list.append(group[i: i + chunk_size])
    return chunk_list

def build_traversal(tree_depth):
    def traverse(node, x, y, w, h, depth=0.0, update_func='update'):
        getattr(node.style, update_func)(x, y, w, h, depth / tree_depth)

        if not len(node.children):
            return

        num_row = int(round(sqrt(len(node.children))))
        row_list = chunk(node.children.values(), num_row)
        if len(row_list) > num_row:
            last = row_list.pop()
            row_list[-1].extend(last)

        len_row_list = len(row_list)
        height = h / len_row_list
        for iy, row in enumerate(row_list):
            row_len = len(row)
            width = w / row_len
            for ix, node in enumerate(row):
                traverse(
                    node,
                    x + ix * width,
                    y + iy * height,
                    width,
                    height,
                    depth + 1.0,
                    update_func)
    return traverse

def build_walker(node, func):
    def walk(node):
        if not func(node):
            return
        for subnode in node.children.values():
            walk(subnode)
    return walk

def as_list(node):
    node_list = []
    def walk(node):
        node_list.append(node)
        for subnode in node.children.values():
            walk(subnode)
    walk(node)
    return node_list

def add_styles(root):
    for node in as_list(root):
        node.build_style()

def child_selection(pos, cursor):
    for child in cursor.children.values():
        if child.collide_point(*pos):
            return child

class Eye(Widget):
    def __init__(self, **kwargs):
        super(Eye, self).__init__(**kwargs)
        self.tree, tree_depth = tree()
        self.cursor = self.tree
        self.traversal = build_traversal(tree_depth)
        add_styles(self.tree)
        self.add_instructions(self.tree)
        self.do_draw('init')
        self.anim_active = False
        self.bind(
            size=self.draw,
            pos=self.draw)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def add_instructions(self, node):
        node.add_instructions(self.canvas)
        for subnode in node.children.values():
            self.add_instructions(subnode)

    def do_draw(self, update_func='update'):
        self.draw(None, None, update_func)

    def draw(self, inst, val, update_func='update'):
        self.traversal(
            self.cursor,
            float(self.x),
            float(self.y),
            float(self.width),
            float(self.height),
            update_func=update_func)

    def on_mouse_pos(self, window, mouse_pos):
        pass
        # def check(node):
        #     return node.check_highlight(*mouse_pos)
        # build_walker(self.cursor, check)(self.cursor)

    def collapse_singles(self, pos):
        selected_child = child_selection(pos, self.cursor)
        if not selected_child:
            return None

        while len(selected_child.children) == 1:
            selected_child = child_selection(pos, selected_child)
        return selected_child

    def redraw_at_cursor(self):
        self.canvas.clear()
        self.add_instructions(self.cursor)
        self.do_draw()

    def on_touch_down(self, touch):
        if not all(['button' in touch.profile, 'pos' in touch.profile]):
            print 'unsupported input type'
            return

        if not self.collide_point(*touch.pos):
            return False

        if self.anim_active:
            return True

        if touch.button == 'left':
            selected_child = self.collapse_singles(touch.pos)
            if not selected_child:
                return True

            def on_zoom_in_complete(anim, zoomer):
                zoomer.reset_zoom()
                self.cursor = selected_child
                self.redraw_at_cursor()
                self.anim_active = False

            self.parent.parent.zoom_in(selected_child).bind(
                on_complete=on_zoom_in_complete)
            self.anim_active = True
            return True

        elif touch.button == 'right':
            cursor_is_root = False
            old_cursor = self.cursor
            self.cursor = old_cursor.parent
            if self.cursor is None:
                cursor_is_root = True
                self.cursor = old_cursor

            while len(self.cursor.children) == 1:
                temp_cursor = self.cursor
                self.cursor = self.cursor.parent
                if self.cursor is None:
                    cursor_is_root = True
                    self.cursor = temp_cursor
                    break

            self.redraw_at_cursor()
            if cursor_is_root:
                return True

            zoomer = self.parent.parent
            anchor = old_cursor.center()
            args = zoomer.calc_zoom_in_target(old_cursor)
            zoomer.reset_props(*args)
            zoomer.apply_zoom_transform(*(args + (anchor,)))
            def on_zoom_out_complete(anim, zoomer):
                self.anim_active = False
            zoomer.zoom_out(old_cursor).bind(
                on_complete=on_zoom_out_complete)
            self.anim_active = True
            return True



