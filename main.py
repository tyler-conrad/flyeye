
from kivy.app import App

from view.zoomer import Zoomer
from view.eye import Eye

class FlyEye(App):
    def build(self):
        zoomer = Zoomer()
        zoomer.add_widget(Eye())
        return zoomer

def main():
    FlyEye().run()

if __name__ == '__main__':
    main()