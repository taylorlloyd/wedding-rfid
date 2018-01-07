import pygame
import time
from pygame import Rect
from views import View, Window, TextView, Button, ProgressView

black = (0, 0, 0)
white = (255, 255, 255)
result_yellow = (252,220,82)
text_font = pygame.font.SysFont("dejavusans", 32)
team_font = pygame.font.SysFont("dejavusans", 48)
name_font = pygame.font.SysFont("dejavusans", 38)
rule_font = pygame.font.SysFont("dejavusans", 32)
team_color = {'Groom': (66,134,244),'Bride': (255,127,127)}
bg_color = {'Groom':(175,223,253),'Bride':(249,218,221)}

class FlipResult(Window):

    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(PasswordWindow())

    def setActive(self, surface, manager):
        super(FlipResult, self).setActive(surface, manager)
        
    def __init__(self, displayText, percentDone):
        super(FlipResult, self).__init__(background_color=result_yellow)
        self.progress = ProgressView(percent_done = percentDone)
        self.text = TextView(displayText, font=text_font)
        self.addView(Rect(0,0,320,445), self.text)
        self.addView(Rect(0,445,320,35), self.progress)
    def __str__(self):
        return "<FlipResultWindow>"

class FlipStatus(Window):
    def launchStatus(self):
        self.launch(StatusPage())

    def launchWifiSetup(self):
        self.launch(PasswordWindow())

    def setActive(self, surface, manager):
        super(FlipStatus, self).setActive(surface, manager)
        #time.sleep(3)
        #self.finish()

    def __init__(self, name, team, rule):
        super(FlipStatus, self).__init__(background_color=bg_color[team])
        self.team = TextView(team + "'s Team", background_color=team_color[team],font=team_font)
        self.name = TextView(name, font=name_font)
        self.rule = TextView("You can convert " + rule, font=rule_font)
        self.progress = ProgressView(percent_done = 1.0)
        self.addView(Rect(0,0,320,60), self.team)
        self.addView(Rect(0,60,320,100), self.name)
        self.addView(Rect(0,160,320,320), self.rule)
        self.addView(Rect(0,445,320,35), self.progress)
    
    def __str__(self):
        return "<FlipStatusWindow>"
        

        

        
