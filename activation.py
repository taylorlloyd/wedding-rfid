import pygame
import time
from pygame import Rect
from views import View, Window, TextView, Button

black = (0, 0, 0)
white = (255, 255, 255)
text_font = pygame.font.SysFont("monospace", 24)
team_font = pygame.font.SysFont("dejavusans", 48)
name_font = pygame.font.SysFont("dejavusans", 38)
rule_font = pygame.font.SysFont("dejavusans", 32)
team_color = {'Groom': (66,134,244),'Bride': (255,127,127)}
bg_color = {'Groom':(175,223,253),'Bride':(249,218,221)}

class Activation(Window):

    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(PasswordWindow())

    def setActive(self, surface, manager):
        super(Activation, self).setActive(surface, manager)
        time.sleep(3.5)
        self.finish()
        
    def __init__(self, name, team, rule):
        super(Activation, self).__init__(background_color=bg_color[team])
        self.team = TextView(team + "'s Team", background_color=team_color[team],font=team_font)
        self.name = TextView(name, font=name_font)
        self.rule = TextView("You can convert " + rule, font=rule_font)
        self.addView(Rect(0,0,320,60), self.team)
        self.addView(Rect(0,60,320,100), self.name)
        self.addView(Rect(0,160,320,320), self.rule)
        

    
    def __str__(self):
        return "<ActivationWindow>"
