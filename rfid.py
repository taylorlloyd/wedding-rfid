from select import select
import pygame

tagCallbacks = []

def add_rfid_callback(cb_fn):
    tagCallbacks.append(cb_fn)

def rfid_keyboard_loop():
    while True:
        print("Enter tag now:\n")
        tag = raw_input()
        for cb in tagCallbacks:
            cb(tag)

def rfid_loop():
    tag = ""
    while True:
      for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_0:
	    tag += "0"
          if e.key == pygame.K_1:
	    tag += "1"
          if e.key == pygame.K_2:
	    tag += "2"
          if e.key == pygame.K_3:
	    tag += "3"
          if e.key == pygame.K_4:
	    tag += "4"
          if e.key == pygame.K_5:
	    tag += "5"
          if e.key == pygame.K_6:
	    tag += "6"
          if e.key == pygame.K_7:
	    tag += "7"
          if e.key == pygame.K_8:
	    tag += "8"
          if e.key == pygame.K_9:
	    tag += "9"
          if e.key == pygame.K_RETURN:
            for cb in tagCallbacks:
              cb(tag)
              tag = ""
                  
