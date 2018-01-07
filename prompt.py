import pygame
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("dejavusans", 48)

class ActivationPrompt(Window):    
    def __init__(self):
        super(ActivationPrompt, self).__init__()
        self.prompt = TextView("Please Scan Your Card To Activate!", font=text_font)
        self.addView(Rect(0,100,320,200), self.prompt)
    
    def __str__(self):
        return "<PromptWindow>"


class FlipperPrompt(Window):    
    def __init__(self):
        super(FlipperPrompt, self).__init__()
        self.prompt = TextView("Please Scan Your Card!", font=text_font)
        self.addView(Rect(0,160,320,120), self.prompt)
    
    def __str__(self):
        return "<FlipperWindow>"
    
