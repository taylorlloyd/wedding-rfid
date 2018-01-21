from rfid import rfid_loop, rfid_keyboard_loop, add_rfid_callback
from display import DisplayManager
import pygame
import threading
import os
import time
import urllib2
import json
import sys
import socket
from prompt import ActivationPrompt
from prompt import FlipperPrompt
from activation import Activation
from loading import Loading
from waiting import Waiting
from flip_result import FlipResult
from flip_result import FlipStatus

partnerResultDict = {True:"%s joined team %s!%s", False:"%s cannot join team %s. %s"}
userResultDict = {True:"Your team was switched to team %s!", False:"You remain on team %s."}

# Create new pygame event
TAGEVENT = pygame.USEREVENT + 1

# Point to the correct framebuffer for this screen
os.environ["SDL_FBDEV"] = "/dev/fb1"

MODE = 'activator'
if len(sys.argv) > 1:
    argument = sys.argv[1]
    if argument == 'activator' or argument == 'master' or argument == 'slave' or argument == 'test':
        MODE = argument    
    else:
        raise Exception("Unknown argument to the program")
    if argument == 'slave':
        if len(sys.argv) < 2:
            raise Exception("Slave requires master IP")
        masterip = sys.argv[2]
    
print "Starting in mode: " + MODE    
# Start watching for RFID events
rfid_thread = threading.Thread(target=rfid_keyboard_loop)
rfid_thread.daemon = True
rfid_thread.start()
load_window = Loading("Loading, Please wait!")
connect_window = Loading("Connecting, Please wait!")
wait_window = Waiting()# if MODE == 'slave' else Waiting(10)

def print_tag_callback(tag):
    print "Tag: %s" % tag
    
#
def activate_tag_callback(tag):
    if display_manager.active_window() != prompt:
        return
    print "Activating tag: %s" % tag
    display_manager.launch(load_window)
    res = urllib2.urlopen("http://192.168.1.10:8000/api/activate?tag=%s" % tag).read()
    print res
    res_dict = json.loads(res)
    if (res_dict["status"] == "error"):
        load_window.finish()
    else:
        name = res_dict["player"]["first_name"] + " " + res_dict["player"]["last_name"]
        team = res_dict["player"]["team"]
        rule = res_dict["player"]["rule_text"]
        activation = Activation(name, team, rule)
        display_manager.launch_consume(activation)
        
#
def master_tag_callback(tag):
    if display_manager.active_window() != prompt:
        return
    print "Master gets tag: %s" % tag
    display_manager.launch(wait_window)
    # 1. Process and pair and acquire partner tag
    received = False
    while not received:
        conn.settimeout(10)
        try:
            data_incoming = conn.recv(4096)
        except:
            conn.settimeout(None)
            wait_window.finish()
            return
        conn.settimeout(None)
        if '}{' in data_incoming:
            data_incoming = '{' + data_incoming.split('}{')[-1]
        partner_payload = json.loads(data_incoming)
        partner_time = partner_payload['time']
        user_time = partner_time - drift
        if time.time() - user_time <= 10:
            received = True
            partner_tag = partner_payload['tag']
            print "Last item in pipeline is not stale"
        else:
            print "Last item in pipeline is stale"
    
    if len(partner_tag) > 10:
        print "Stale tags found!"
        partner_tag = partner_tag[len(partner_tag)-10:]
    partner_time = partner_payload['time']
    print "Partner tag:"
    print partner_tag
    
    
    # 2. Send http request to server
    res = urllib2.urlopen("http://192.168.1.10:8000/api/interact?player1=%s&player2=%s" % (tag, partner_tag)).read()
    # 3. Send result to the slave
    conn.send(res)
    # 4. Display 3-window result
    # Master is player 1, send player 2 result to partner PI
    print res
    res_dict = json.loads(res)
    if (res_dict["status"] == "error"):
        wait_window.finish()
    else:
        playerChanged = res_dict["player1_changed"]
        partnerChanged = res_dict["player2_changed"]
        name = res_dict["player1"]["first_name"] + " " + res_dict["player1"]["last_name"]
        team = res_dict["player1"]["team"]
        rule = res_dict["player1"]["rule_text"]
        flipUserResult = FlipResult(userResultDict[playerChanged] % team,0.33)
        flipPartnerResult = FlipResult(partnerResultDict[partnerChanged] % (res_dict["player2"]["first_name"], res_dict["player2"]["team"],res_dict["player1_reason"]),0.66)
        flipStatus = FlipStatus(name, team, rule)
        display_manager.launch_consume(flipUserResult)
        time.sleep(3)
        display_manager.launch_consume(flipPartnerResult)
        time.sleep(3)
        display_manager.launch_consume(flipStatus)
        time.sleep(4)
        flipStatus.finish()
    

def slave_tag_callback(tag):
    if display_manager.active_window() != prompt:
        return
    print "Slave gets tag: %s" % tag
    display_manager.launch(wait_window)
    payload = {"tag":tag, "time":time.time()}
    ss.send(json.dumps(payload))
    ss.settimeout(10)
    try:
        res = ss.recv(4096)
    except:
        ss.settimeout(None)
        wait_window.finish()
        return
    ss.settimeout(None)
    res_dict = json.loads(res)
    if (res_dict["status"] == "error"):
        wait_window.finish()
    else:
        playerChanged = res_dict["player2_changed"]
        partnerChanged = res_dict["player1_changed"]
        name = res_dict["player2"]["first_name"] + " " + res_dict["player2"]["last_name"]
        team = res_dict["player2"]["team"]
        rule = res_dict["player2"]["rule_text"]
        flipUserResult = FlipResult(userResultDict[playerChanged] % team,0.33)
        flipPartnerResult = FlipResult(partnerResultDict[partnerChanged] % (res_dict["player1"]["first_name"],res_dict["player1"]["team"],res_dict["player2_reason"]),0.66)
        flipStatus = FlipStatus(name, team, rule)
        display_manager.launch_consume(flipUserResult)
        time.sleep(3)
        display_manager.launch_consume(flipPartnerResult)
        time.sleep(3)
        display_manager.launch_consume(flipStatus)
        time.sleep(4)
        flipStatus.finish()
    
HOST='0.0.0.0'
PORT=2217    
if MODE == 'activator':
    add_rfid_callback(activate_tag_callback)
elif MODE == 'master':
    add_rfid_callback(master_tag_callback)
    ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Bounding to socket"

    bound = False
    while not bound:
        try:
            ms.bind((HOST,PORT))
            bound = True
        except:
            time.sleep(1)
            pass
    print ("Socket bound.")
    #Start listening
    ms.listen(10)
    print ("Socket Listening")
    conn, addr = ms.accept()
    print ("Slave connected!")
    print "Waiting for slave timestamp"
    slavetime = conn.recv(256)
    drift = float(slavetime) - time.time()
    print "Drift: " + str(drift)
    
elif MODE == 'slave':
    add_rfid_callback(slave_tag_callback)
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    print "Attempting to connect to master..."
    while not connected:
        try:
            ss.connect((masterip, PORT))
            connected = True
        except:
            time.sleep(0.5)
            pass
    print "Connected to master at " + masterip
    print "Sending master slave time-stamp"
    ss.send(str(time.time()))
    
elif MODE == 'test':
    add_rfid_callback(print_tag_callback)
    
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
