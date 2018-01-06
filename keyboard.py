from views import View, Button
from pygame import Rect

bg_color = (0, 0, 0)
key_color = (40, 40, 40)
txt_color = (255, 255, 255)
backsp = "\u21A9"
enter = "Enter"
shift = "\u21E7"
num = "123"
space = " "
btn_width = 340/11
btn_height = 40

keys = [[(1,"q","Q","1"),(1,"w","W","2"),(1,"e","E","3"),
         (1,"r","R","4"),(1,"t","T","5"),(1,"y","Y","6"),
         (1,"u","U","7"),(1,"i","I","8"),(1,"o","O","9"),
         (1,"p","P","0"),(1,backsp,None,None)],
         [(0.5,None,None,None),(1,"a","A","-"),(1,"s","S","/"),
             (1,"d","D",":"),(1,"f","F",";"),(1,"g","G","("),
         (1,"h","H",")"),(1,"j","J","$"),(1,"k","K","&"),
         (1,"l","L","@"),(1.5,enter,None,None)],
         [(1,shift,None,None),(1,"z","Z","\""),(1,"x","X","_"),
         (1,"c","C","["),(1,"v","V","]"),(1,"b","B","?"),
         (1,"n","N","%"),(1,"m","M","*"),(1,",","!","^"),
         (1,".","?","\\"),(1,shift,None,None)],
         [(3,num,None,None),(6,space,None,None),(2,num,None,None)]]

class Keyboard(View):

    def __init__(self):
        super(Keyboard, self).__init__(background_color=bg_color)
        self.buttons = []
        self.mode = "bare"
        y_off = 0
        for row in keys:
            x_off = 0
            for (width, bare_k, shift_k, num_k) in row:
                if bare_k is not None:
                    btn = Key(self, bare_k, shift_k, num_k)
                    self.buttons.append(btn)
                    self.addView(Rect(x_off+2, y_off+2, btn_width*width-4, btn_height-4), btn)
                x_off += btn_width*width
            y_off += btn_height

    def setMode(self, mode):
        self.delayRender(True)
        self.mode = mode
        for btn in self.buttons:
            if mode == "bare":
                btn.setText(btn.bare_k)
            elif mode == "shift":
                if btn.shift_k is None:
                    btn.setText(btn.bare_k)
                else:
                    btn.setText(btn.shift_k)
            else:
                if btn.num_k is None:
                    btn.setText(btn.bare_k)
                else:
                    btn.setText(btn.num_k)
        self.delayRender(False)

    def onKeyPress(self,key):
        if key == shift:
            if self.mode == "bare":
                self.setMode("shift")
            else:
                self.setMode("bare")
        elif key == num:
            if self.mode == "num":
                self.setMode("bare")
            else:
                self.setMode("num")
        else:
            print(key)

class Key(Button):
    def onKeyPress(self):
        self.keyboard.onKeyPress(self.text)

    def __init__(self,keyboard,bare_k,shift_k,num_k):
        super(Key,self).__init__(bare_k, on_click=self.onKeyPress,
                background_color=key_color, foreground_color=txt_color)
        self.keyboard = keyboard
        self.bare_k = bare_k
        self.shift_k = shift_k
        self.num_k = num_k
