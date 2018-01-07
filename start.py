from rfid import rfid_loop, add_rfid_callback
from display import DisplayManager
import pygame
import threading
import os
import time
import urllib2
import json
import sys
from prompt import ActivationPrompt
from prompt import FlipperPrompt
from activation import Activation
from loading import Loading
from waiting import Waiting
# Create new pygame event
TAGEVENT = pygame.USEREVENT + 1

# Point to the correct framebuffer for this screen
os.environ["SDL_FBDEV"] = "/dev/fb1"

MODE = 'activator'
if len(sys.argv) > 1:
    argument = sys.argv[1]
    if argument == 'activator' or argument == 'master' or argument == 'slave':
        MODE = argument
    else:
        raise Exception("Unknown argument to the program")

print "Starting in mode: " + MODE    
# Start watching for RFID events
rfid_thread = threading.Thread(target=rfid_loop)
rfid_thread.daemon = True
rfid_thread.start()
load_window = Loading()
wait_window = Waiting()

# {"status": "ok", "player": {"first_name": "Madison", "last_name": "Olthof", "tag": "A", "team": "Groom", "rule_text": "Maddy's relatives"}}
def activate_tag_callback(tag):
    print "Activating tag: %s" % tag
    display_manager.launch(load_window)
    res = urllib2.urlopen("http://192.168.1.112:8000/api/activate?tag=%s" % tag).read()
    print res
    res_dict = json.loads(res)
    if (res_dict["status"] == "error"):
        load.finish()
    else:
        name = res_dict["player"]["first_name"] + " " + res_dict["player"]["last_name"]
        team = res_dict["player"]["team"]
        rule = res_dict["player"]["rule_text"]
        activation = Activation(name, team, rule)
        display_manager.launch_consume(activation)
        
def master_tag_callback(tag):
    print "Master does nothing with tag: %s" % tag
    display_manager.launch(wait_window)

def slave_tag_callback(tag):    
    print "Master does nothing with tag: %s" % tag
        
if MODE == 'activator':
    add_rfid_callback(activate_tag_callback)
elif MODE == 'master':
    add_rfid_callback(master_tag_callback)
elif MODE == 'slave':
    add_rfid_callback(slave_tag_callback)

# Create the pygame screen
pygame.init()

#"Ininitializes a new pygame screen using the framebuffer"
# Based on "Python GUI in Linux frame buffer"
disp_no = os.getenv("DISPLAY")
if disp_no:
    print "I'm running under X display = {0}".format(disp_no)
    
# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
            continue
        found = True
        break
    
    if not found:
        raise Exception('No suitable video driver found!')
        
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print "Framebuffer size: %d x %d" % (size[0], size[1])
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
# Clear the screen to start
screen.fill((0, 0, 0))
# Initialise font support
pygame.font.init()
# Render the screen
pygame.display.flip()
# Hide the cursor
pygame.mouse.set_visible(0)

prompt = ActivationPrompt() if MODE == 'activator' else FlipperPrompt()

display_manager = DisplayManager(screen, prompt)
display_thread = threading.Thread(target=display_manager.activity_loop)
display_thread.daemon = True
display_thread.start()

while(True):
    continue
