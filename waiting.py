import pygame
import time
import threading
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("dejavusans", 32)

def finishTimer(seconds, view):
        time.sleep(seconds)
        
        view.finish()

class Waiting(Window):
        
    # def setActive(self, surface, manager):
    #     super(Waiting, self).setActive(surface, manager)
    #     timerThread = threading.Thread(target=finishTimer, args=(self.timeout,self,))
    #     timerThread.start()
    
    def __init__(self):
        super(Waiting, self).__init__(background_color=black)
        #self.timeout = timeout
        self.waiting = TextView("Awaiting partner...", font=text_font, foreground_color=white, background_color=black)
        self.addView(Rect(0,140,320,200), self.waiting)
    
    def __str__(self):
        return "<WaitingWindow>"
