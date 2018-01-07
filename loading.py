import pygame
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("dejavusans", 32)

class Loading(Window):
    
    def __init__(self):
        super(Loading, self).__init__()
        self.loading = TextView("Loading, Please wait!", font=text_font)
        self.addView(Rect(0,140,320,200), self.loading)
    
    def __str__(self):
        return "<LoadingWindow>"
