import pygame
from pygame import Rect
from views import View, Window, TextView, Button
from status import StatusPage
from wifisetup import PasswordWindow

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("monospace", 24)

class Menu(Window):

    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(PasswordWindow())

    def __init__(self):
        super(Menu, self).__init__()
        self.tv = TextView("Menu")
        self.status = Button("System Status", on_click=self.launchStatus)
        self.wifi_setup = Button("Wifi Setup", on_click=self.launchWifiSetup)
        self.addView(Rect(60,0,200,40), self.tv)
        self.addView(Rect(60,100,200,40), self.status)
        self.addView(Rect(60,200,200,40), self.wifi_setup)

    def onTouch(self, x, y):
        print("Touch at " + str(x)+ ", "+str(y))
        return True;

    def __str__(self):
        return "<MenuWindow>"
