#!/usr/bin/python3

from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener


class EventHandler:
    """ Collects the events from mouse and keyboard. """
    def __init__(self):
        self.mouse = {'x':0, 'y':0, 'distance':0, 'button':'', 'scroll':0}
        self.keyboard = {}
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mlistener, KeyListener(on_press=self.on_press, on_release=self.on_release) as self.klistener:
            self.mlistener.join()
            self.klistener.join()
    
    def on_move(self, x, y):
        """ Read mouse movements and track the distance of the movements. """
        dx = abs(self.mouse['x'] - x)
        dy = abs(self.mouse['y'] - y)
        self.mouse['x'] = x
        self.mouse['y'] = y
        distance = dx + dy
        self.mouse['distance'] = self.mouse['distance'] + distance
        distance_m = self.mouse['distance'] * 0.00026458333
#        print(f"{distance_m} m")

    def on_click(self, x, y, button, pressed):
        """ Read mouse clicks and record values. """
        self.mouse['x'] = x
        self.mouse['y'] = y
        self.mouse['button'] = button
        if str(button) == 'Button.right':
            self.mouse['button'] = 'right'
        elif str(button) == 'Button.middle':
            self.mouse['button'] = 'middle'
        else:
            self.mouse['button'] = 'left'
        print(f"Clicked at: {x},{y}, {self.mouse['button']} used.")
        print(f"Scrolled: {self.mouse['scroll']}, total distance moved: {self.mouse['distance']}.")

    def on_scroll(self, x, y, dx, dy):
        """ Read mouse scrolls and calculate the total amount of scrolls."""
        self.mouse['scroll'] += dy 

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


events = EventHandler()


