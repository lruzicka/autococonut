#!/usr/bin/python3

from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener


class EventCollector:
    """ Collects the events from mouse and keyboard. """
    def __init__(self):
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as self.mlistener, KeyListener(on_press=self.on_press, on_release=self.on_release) as self.klistener:
            self.mlistener.join()
            self.klistener.join()
    
    def on_move(self, x, y):
        print(x, y)

    def on_click(self, x, y, button, pressed):
        print(x, y, button, pressed)

    def on_scroll(self, x, y, dx, dy):
        print(x, y, dx, dy)

    def on_press(self, key):
        print(key)

    def on_release(self, key):
        print(f"{key} R")
        if key == Key.f10:
            self.mlistener.stop()
            return False


events = EventCollector()


