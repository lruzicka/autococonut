#!/usr/bin/python3

from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener


class EventCollector:
    """ Collects the events from mouse and keyboard. """
    def __init__(self):
        self.mouse = {'x':0, 'y':0, 'distance':0}
        self.keyboard = {}
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mlistener, KeyListener(on_press=self.on_press, on_release=self.on_release) as self.klistener:
            self.mlistener.join()
            self.klistener.join()
    
    def on_move(self, x, y):
        """ Read mouse movements, updates the mouse position and calculates the distance of the mouse track. """
        dx = abs(self.mouse['x'] - x)
        dy = abs(self.mouse['y'] - y)
        self.mouse['x'] = x
        self.mouse['y'] = y
        distance = dx + dy
        self.mouse['distance'] = self.mouse['distance'] + distance
        distance_m = self.mouse['distance'] * 0.00026458333
        print(f"{distance_m} m")

    def on_click(self, x, y, button, pressed):
        """ Read mouse clicks. """
        print(x, y, button, pressed)

    def on_scroll(self, x, y, dx, dy):
        """ Read mouse scrolls."""
        print(x, y, dx, dy)

    def on_press(self, key):
        """ Read keyboard presses. """
        print(key)

    def on_release(self, key):
        """ Read keyboard releases. """
        print(f"{key} R")
        # The F10 key terminates the listeners.
        if key == Key.f10:
            self.mlistener.stop()
            return False


events = EventCollector()


