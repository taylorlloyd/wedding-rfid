import pygame
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("monospace", 24)

class Menu(Window):

    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(StatusPage())

    def __init__(self):
        super(Menu, self).__init__()
        self.tv = TextView("Test String")
        self.status = Button("System Status", on_click=self.launchStatus)
        self.wifi_setup = Button("Wifi Setup", on_click=self.launchWifiSetup)
        self.addView(Rect(10,0,320,40), self.tv)
        self.addView(Rect(10,50,320,40), self.status)
        self.addView(Rect(10,100,320,40), self.wifi_setup)

    def onTouch(self, x, y):
        print("Touch at " + str(x)+ ", "+str(y))
        return True;

    def __str__(self):
        return "<MenuWindow>"
