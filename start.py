from rfid import rfid_loop, add_rfid_callback
from display import DisplayManager
import pygame
import threading

# Start watching for RFID events
rfid_thread = threading.Thread(target=rfid_loop)
rfid_thread.daemon = True
rfid_thread.start()

def print_tag(tag):
    print("Tag: " + tag)

add_rfid_callback(print_tag)

# Create the pygame screen
pygame.init()
(width, height) = (340, 480)
screen = pygame.display.set_mode((width, height))

from menu import Menu
menu = Menu()

display_manager = DisplayManager(screen, menu)
display_thread = threading.Thread(target=display_manager.activity_loop)
display_thread.daemon = True
display_thread.start()

while(True):
    continue
