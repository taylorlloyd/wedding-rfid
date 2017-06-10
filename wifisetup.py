from views import Window
from keyboard import Keyboard
from pygame import Rect

class PasswordWindow(Window):
    def __init__(self):
        super(PasswordWindow, self).__init__()
        self.kb = Keyboard()
        self.addView(Rect(0,320,340,160), self.kb)
