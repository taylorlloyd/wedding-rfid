import pygame
import traceback
from pygame import Rect

pygame.font.init()
default_font = pygame.font.SysFont("ubuntu", 24)

class View(object):
    def __init__(self, background_color=None, foreground_color=(0,0,0)):
        self.parent = None
        self.subviews = []
        self.background_color = background_color
        self.foreground_color = foreground_color

    def render(self, surface):
        pass

    def onTouch(self, x, y):
        return False

    def onParentAdded(self):
        pass

    def rerender(self):
        if self.parent is not None:
           self.parent.rerender()

    def render_internal(self, surface):
        if self.background_color is not None:
            surface.fill(self.background_color)
        try:
            self.render(surface)
        except:
            traceback.print_exc()
        for (r, v) in self.subviews:
            v.render_internal(surface.subsurface(r))

    def onTouch_internal(self, x, y):
        for (r, v) in self.subviews:
            if(r.collidepoint(x,y)):
                if v.onTouch_internal(x-r.x, y-r.y):
                    return True
        try:
            return self.onTouch(x, y)
        except:
            traceback.print_exc()
        return False

    def addView(self, rect, view):
        self.subviews.append((rect, view))
        view.parent = self
        view.onParentAdded()

    def __str__(self):
        return "<View (" + str(len(self.subviews)) + " children)>"

class Window(View):
    def __init__(self):
        super(Window, self).__init__(background_color=(255,255,255))
        self.surface = None
        self.manager = None

    def setActive(self, surface, manager):
        self.surface = surface
        self.manager = manager
        self.rerender()

    def setInactive(self):
        self.surface = None
        self.manager = None

    def rerender(self):
        if self.surface is not None:
            self.render_internal(self.surface)
            pygame.display.flip()

    def finish(self):
        self.manager.finish()

    def launch(self, window):
        self.manager.launch(window)

    def __str__(self):
        return "<Window (" + str(len(self.subviews)) + " children)>"


class TextView(View):

    def __init__(self, text, background_color=None, foreground_color=(0,0,0), font=default_font):
        super(TextView, self).__init__(background_color, foreground_color)
        self.text = text
        self.font = font

    def setText(self, text):
        self.text = text
        self.rerender()

    def render(self, surface):
        txt_surf = self.font.render(self.text, 1, self.foreground_color)
        # Center the text
        (t_width, t_height) = txt_surf.get_size()
        (s_width, s_height) = surface.get_size()
        x_off = (s_width-t_width)/2
        y_off = (s_height-t_height)/2
        surface.blit(txt_surf, (x_off, y_off) )

    def __str__(self):
        return "<TextView \"" + self.text + "\">"

class Button(TextView):
    def __init__(self, text, on_click=None,
                 background_color=(200,200,200),
                 foreground_color=(0,0,0),
                 font=default_font):
        super(Button, self).__init__(text, background_color=background_color,
                                           foreground_color=foreground_color,
                                           font=default_font)
        self.on_click = on_click

    def onTouch(self, x, y):
        if self.on_click is not None:
            self.on_click()
        return True

    def __str__(self):
        return "<Button \"" + self.text + "\">"
