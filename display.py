import pygame
import traceback

class DisplayManager(object):
    def __init__(self, surface, root_window):
        self.surface = surface
        self.window_stack = [root_window];
        self.window_stack[-1].setActive(self.surface, self)

    def finish(self):
        if len(self.window_stack) > 1:
            try:
                self.window_stack[-1].setInactive()
            except:
                traceback.print_exc()
            self.window_stack.pop()
            try:
                self.window_stack[-1].setActive(self.surface, self)
            except:
                traceback.print_exc()

    def launch_consume(self, window):
        try:
            self.window_stack[-1].setInactive()
        except:
            traceback.print_exc()
        self.window_stack.pop()
        self.window_stack.append(window)
        try:
            self.window_stack[-1].setActive(self.surface, self)
        except:
            traceback.print_exc()
                
    def launch(self, window):
        try:
            self.window_stack[-1].setInactive()
        except:
            traceback.print_exc()
        self.window_stack.append(window)
        try:
            self.window_stack[-1].setActive(self.surface, self)
        except:
            traceback.print_exc()

    def activity_loop(self):
        while True:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    self.window_stack[-1].onTouch_internal(x,y)

