import pygame
from pygame import Rect
from views import View, Window, TextView, Button
from rfid import add_rfid_callback
import threading
import socket

class StatusPage(Window):

    def setTag(self, tag):
        self.tag = tag
        self.tag_txt.setText("Last RFID Tag: " + self.tag)

    def __init__(self):
        super(StatusPage, self).__init__()
        self.connected = "Unknown"
        self.ip = "Unknown"
        self.tag = "None"
        self.title = TextView("Status Page")
        self.back = Button("Back", on_click=self.finish)
        self.conn_txt = TextView("Inet Status: "+self.connected)
        self.ip_txt = TextView("IP Address: "+self.ip)
        self.tag_txt = TextView("Last RFID Tag: "+self.tag)

        self.addView(Rect(10,0,320,40), self.title)
        self.addView(Rect(10,50,320,40), self.conn_txt)
        self.addView(Rect(10,100,320,40), self.ip_txt)
        self.addView(Rect(10,150,320,40), self.tag_txt)
        self.addView(Rect(10,430, 320, 40), self.back)

        add_rfid_callback(self.setTag)

    def setActive(self, surface, manager):
        self.connected = "Unknown"
        self.ip = "Unknown"
        super(StatusPage, self).setActive(surface, manager)
        status_thread = threading.Thread(target=self.statusTest)
        status_thread.daemon = True
        status_thread.start()

    def setInactive(self):
        super(StatusPage, self).setInactive()

    def statusTest(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 53))
            self.connected = "Connected"
            self.ip = s.getsockname()[0]
        except:
            self.connected = "Disconnected"
            self.ip = "None"
        self.conn_txt.setText("Inet Status: "+self.connected)
        self.ip_txt.setText("IP Address: "+self.ip)

