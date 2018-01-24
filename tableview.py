import pygame
import time
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("monospace", 24)
name_font = pygame.font.SysFont("dejavusans", 38)
table_font = pygame.font.SysFont("dejavusans", 48)
tnum_font = pygame.font.SysFont("dejavusans", 72)

class TableWindow(Window):

    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(PasswordWindow())

    def setActive(self, surface, manager):
        super(Activation, self).setActive(surface, manager)
        time.sleep(3.5)
        self.finish()

    def __init__(self, name, table):
        super(Activation, self).__init__(background_color=white)
        self.name = TextView(name, font=name_font)
        self.table = TextView("Table", font=table_font)
        self.tnum = TextView(str(table), font=tnum_font)
        self.addView(Rect(0,30,320,60), self.name)
        self.addView(Rect(0,160,320,60), self.table)
        self.addView(Rect(0,220,320,100), self.tnum)


    def __str__(self):
        return "<TableWindow>"
