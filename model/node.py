from kivy.graphics import Rectangle
from kivy.graphics import Color

BORDER_SIZE = 0.25

class Style(object):
    def __init__(self):
        self.outer_color = Color(0.0, 0.0, 0.0, 1.0)
        self.inner_color = Color(0.0, 0.0, 0.0, 1.0)
        self.outer_rect = Rectangle()
        self.inner_rect = Rectangle()

    def update(self, x, y, w, h, depth):
        self.depth_color = (depth,) * 3 + (1.0,)
        self.inner_color.rgb = self.depth_color
        self.outer_rect.pos = (x, y)
        self.outer_rect.size = (w, h)
        self.inner_rect.pos = (x + BORDER_SIZE, y + BORDER_SIZE)
        self.inner_rect.size = (w - (BORDER_SIZE * 2.0), h - (BORDER_SIZE * 2.0))

class NodeStyle(Style):
    pass


class LeafStyle(Style):
    pass


class Node(object):
    def __init__(self, name, path, parent):
        self.name = name
        self.path = path
        self.parent = parent
        self.children = {}

    def setdefault(self, name, path, parent):
        if name in self.children:
            return self.children[name]
        n = Node(name, path, parent)
        self.children[name] = n
        return n

    def add_instructions(self, canvas):
        canvas.add(self.style.outer_color)
        canvas.add(self.style.outer_rect)
        canvas.add(self.style.inner_color)
        canvas.add(self.style.inner_rect)

    def is_leaf(self):
        return bool(self.children)

    def build_style(self):
        self.style = LeafStyle() if self.is_leaf() else NodeStyle()

    def collide_point(self, x, y):
        rx, ry = self.style.outer_rect.pos
        rw, rh = self.style.outer_rect.size
        return (rx < x <= (rx + rw)) and (ry < y <= (ry + rh))


    def check_highlight(self, mouse_x, mouse_y):
        g, b = self.style.depth_color[1:3]
        self.style.inner_color.rgba = (
            (1.0, g, b, 1.0)
            if self.collide_point(mouse_x, mouse_y)
            else self.style.depth_color)
        return True

    def center(self):
        x, y = self.style.outer_rect.pos
        w, h = self.style.outer_rect.size
        return (x + w / 2.0, y + h / 2.0)