from evdev import InputDevice
from select import select

tagCallbacks = []

def add_rfid_callback(cb_fn):
    tagCallbacks.append(cb_fn)

def rfid_keyboard_loop():
    while True:
        tag = raw_input()
        for cb in tagCallbacks:
            cb(tag)

def rfid_loop():
    keys = "X^1234567890XXXXqwertzuiopXX\nXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
    dev = InputDevice('/dev/input/by-id/usb-Sycreader_USB_Reader_08FF20150112-event-kbd')
    tag = ""
    while True:
        r,w,x = select([dev], [], [])
        for event in dev.read():
            if event.type==1 and event.value==1:
                if event.code == 28:
                    if len(tag) > 8:
                        for cb in tagCallbacks:
                            cb(tag)
                    tag = ""
                else:
                    tag = tag + keys[event.code]
