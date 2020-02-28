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


class Collector:
    """ Collects the events from mouse and keyboard. """
    def __init__(self, handler):
        self.handler = handler
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mlistener, KeyListener(on_press=self.on_press, on_release=self.on_release) as self.klistener:
            self.mlistener.join()
            self.klistener.join()

    def get_key_name(self, key):
        if isinstance(key, KeyCode):
            return key.char
        else:
            return str(key)
    
    def on_move(self, x, y):
        """ Read mouse movements. """
        self.handler.add_to_distance(x, y)

    def on_click(self, x, y, button, pressed):
        """ Read mouse clicks. """
        self.handler.record_mouse_click(x, y, button)
        print(self.handler.cx, self.handler.cy, self.handler.button)
        print(self.handler.create_needle_coordinates())

    def on_scroll(self, x, y, dx, dy):
        """ Read mouse scrolls and calculate the total amount of scrolls."""
        self.handler.add_to_scrolled(dx, dy)

    def on_press(self, key):
        """ Read keyboard presses and record values. """
        print(self.get_key_name(key))

    def on_release(self, key):
        """ Read keyboard releases. """
        print(f"{key} R")
        # The F10 key terminates the listeners.
        if key == Key.f10:
            self.mlistener.stop()
            return False

magicbox = Handler()
events = Collector(magicbox)


