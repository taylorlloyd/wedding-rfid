import pygame

class DisplayManager(object):
    def __init__(self, surface, root_window):
        self.surface = surface
        self.window_stack = [root_window];
        self.window_stack[-1].setActive(self.surface, self)

    def finish(self):
        if len(self.window_stack) > 1:
            self.window_stack[-1].setInactive()
            self.window_stack.pop()
            self.window_stack[-1].setActive(self.surface, self)

    def launch(self, window):
        self.window_stack[-1].setInactive()
        self.window_stack.append(window)
        self.window_stack[-1].setActive(self.surface, self)

    def activity_loop(self):
        while True:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    self.window_stack[-1].onTouch_internal(x,y)
