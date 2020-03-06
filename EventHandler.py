#!/usr/bin/python3

from math import sqrt
from pynput.keyboard import Key, KeyCode
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener

class Handler:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.cx = 0
        self.cy = 0
        self.button = ''
        self.distance = 0
        self.scrollx = 0
        self.scrolly = 0
        self.modified = False
        self.modifier = ''
        self.special = ''
        self.text_buffer = []

    def add_to_distance(self, x, y):
        """ Adds value to the current distance. """
        dx = abs(self.mx - x)
        dy = abs(self.my - y)
        self.mx = x
        self.my = y
        distance = sqrt((dx**2)+(dy**2))
        self.distance = self.distance + distance

    def display_distance(self, unit=None):
        """ Shows the reached distance in px (default), cm, or m. """
        if unit == 'cm':
            distance = round(self.distance * 0.026458333)
        elif unit == 'm':
            distance = round(self.distance * 0.00026458333)
        else:
            distance = self.distance
        return distance

    def add_to_scrolled(self, dx, dy):
        """ Counts how many times a mouse has been scrolled up or down."""
        self.scrollx += dx
        self.scrolly += dy
        return 0

    def record_mouse_click(self, x, y, button):
        """ Records the mouse click values for further processing."""
        self.cx = x
        self.cy = y
        self.button = str(button)
        return 0

    def create_needle_coordinates(self):
        """ Calculates needle coordinates around the click point. """
        lx = self.cx - 20
        rx = self.cx + 20
        ly = self.cy - 10
        ry = self.cy + 10
        coordinates = (lx,ly,rx,ry)
        return(coordinates)

    def press_modifier(self, modifier):
        print(f"Modifier: {modifier}")
        self.modified = True
        self.modifier = modifier

    def release_modifier(self):
        print("Modifier released.")
        self.modified = False
        self.modifier = ''

    def empty_text_buffer(self):
        tbuffer = ''.join(self.text_buffer)
        self.text_buffer = []
        print(f"Buffer: {tbuffer}\n")
        return tbuffer

    def pronounce_move(self):
        pass

    def pronounce_click(self):
        coordinates = self.create_needle_coordinates()
        print(f"{self.button} click on {coordinates}.")

    def pronounce_assert(self):
        coordinates = self.create_needle_coordinates()
        print(f"Check item at {coordinates}.")

    def pronounce_typing(self):
        pass

    def pronounce_shortcut(self):
        print(f"Press {self.modifier}-{self.empty_text_buffer()}.")


class Collector:
    """ Collects the events from mouse and keyboard. """
    def __init__(self, handler):
        self.handler = handler
        self.modifiers = [
                        'Key.alt',
                        'Key.ctrl',
                        'Key.ctrl_r',
                        'Key.shift',
                        'Key.caps_lock',
                        'Key.cmd',
        ]
        self.specials = [
                        'Key.menu',
                        'Key.esc',
                        'Key.backspace',
                        'Key.insert',
                        'Key.home',
                        'Key.page_up',
                        'Key.page_down',
                        'Key.end',
                        'Key.delete',
                        'Key.print_screen',
                        'Key.scroll_lock',
                        'Key.pause',
        ]
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mlistener, KeyListener(on_press=self.on_press, on_release=self.on_release) as self.klistener:
            self.mlistener.join()
            self.klistener.join()

    def get_key_name(self, key):
        """ Convert the Key into a string. """
        if isinstance(key, KeyCode):
            return key.char
        else:
            return str(key)
    
    def on_move(self, x, y):
        """ Read mouse movements and add each move to the total distance. """
        self.handler.add_to_distance(x, y)

    def on_click(self, x, y, button, pressed):
        """ Read mouse clicks. """
        self.handler.record_mouse_click(x, y, button)
        if pressed:
            if self.handler.modified == True and self.handler.modifier == 'Key.ctrl':
                self.handler.pronounce_assert()
            else:
                self.handler.pronounce_click()

    def on_scroll(self, x, y, dx, dy):
        """ Read mouse scrolls and calculate the total amount of scrolls."""
        self.handler.add_to_scrolled(dx, dy)

    def on_press(self, key):
        """ Read keyboard presses and record values. """
        key = self.get_key_name(key)
        if key in self.modifiers:
            self.handler.press_modifier(key)
        if 'Key' not in key: # Only record alphanumeric keys in the buffer.
            self.handler.text_buffer.append(key)

    def on_release(self, key):
        """ Read keyboard releases. """
        if str(key) in self.modifiers:
            self.handler.pronounce_shortcut()
            self.handler.release_modifier()

        print(f"{key} R")
        # The F10 key terminates the listeners.
        if key == Key.f6:
            self.handler.empty_text_buffer()
        elif key == Key.f10:
            self.mlistener.stop()
            return False



#================================================================================
magicbox = Handler()
events = Collector(magicbox)


