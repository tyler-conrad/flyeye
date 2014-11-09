from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix

class Zoomer(ScatterLayout):
    translate_dx = NumericProperty(0.0)
    translate_dy = NumericProperty(0.0)
    scale_dx = NumericProperty(1.0)
    scale_dy = NumericProperty(1.0)

    def __init__(self):
        super(Zoomer, self).__init__(
            do_translation=False,
            do_rotation=False,
            do_scale=False)
        self.anim = None
        self.bind_props()

    def bind_props(self):
        self.bind(
            translate_dx=self.on_zoom_change,
            translate_dy=self.on_zoom_change,
            scale_dx=self.on_zoom_change,
            scale_dy=self.on_zoom_change)

    def unbind_props(self):
        self.unbind(
            translate_dx=self.on_zoom_change,
            translate_dy=self.on_zoom_change,
            scale_dx=self.on_zoom_change,
            scale_dy=self.on_zoom_change)

    def calc_zoom_in_target(self, cursor):
        cursor_width, cursor_height = cursor.style.outer_rect.size
        cursor_center_x, cursor_center_y = cursor.center()
        return (
            -(cursor_center_x - self.center_x),
            -(cursor_center_y - self.center_y),
            self.width / cursor_width,
            self.height / cursor_height)

    def build_anim(self, trans_dx, trans_dy, scale_dx, scale_dy):
        anim = Animation(
            translate_dx=trans_dx,
            translate_dy=trans_dy,
            scale_dx=scale_dx,
            scale_dy=scale_dy,
            duration=0.2,
            transition='out_quint')
        anim.start(self)
        return anim

    def zoom_out(self, old_cursor):
        self.anchor = old_cursor.center()
        return self.build_anim(0.0, 0.0, 1.0, 1.0)

    def zoom_in(self, cursor):
        translate_dx, translate_dy, scale_dx, scale_dy =\
            self.calc_zoom_in_target(cursor)
        self.anchor = cursor.center()
        return self.build_anim(
            translate_dx,
            translate_dy,
            scale_dx,
            scale_dy)

    def reset_props(
            self,
            trans_dx,
            trans_dy,
            scale_dx,
            scale_dy):
        self.unbind_props()
        self.translate_dx = trans_dx
        self.translate_dy = trans_dy
        self.scale_dx = scale_dx
        self.scale_dy = scale_dy
        self.bind_props()

    def reset_zoom(self):
        self.transform = Matrix()
        self.reset_props(0.0, 0.0, 1.0, 1.0)

    def on_zoom_change(self, inst, val):
        self.apply_zoom_transform(
            self.translate_dx,
            self.translate_dy,
            self.scale_dx,
            self.scale_dy,
            self.anchor)

    def apply_zoom_transform(
            self,
            translate_dx,
            translate_dy,
            scale_dx,
            scale_dy,
            anchor):

        self.apply_transform(self.transform_inv)

        self.apply_transform(Matrix().scale(
            scale_dx,
            scale_dy,
            1.0), anchor=anchor)

        self.apply_transform(Matrix().translate(
            translate_dx,
            translate_dy,
            1.0))
