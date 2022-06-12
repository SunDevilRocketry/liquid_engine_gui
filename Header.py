# !/usr/bin/env python3
from tkinter import *

class Header:

    def __init__(self, root, background, text, width, height, size):
        self.c = Canvas(root, width=width, height=height, bg=background, highlightthickness=0)
        self.width = width
        self.height = height

        self.c.create_line((width / 8.0, 7 * height / 8.0), (7 * width / 8.0, 7 * height / 8.0), width=1, fill='white')
        self.c.create_text(width / 2.0, height / 2.0, font=("Arial", size, ''), fill="white", text=text)

    def getWidget(self):
        return self.c

class Text:

    def __init__(self, root, background, text, width, height, size):
        self.c = Canvas(root, width=width, height=height, bg=background, highlightthickness=0)
        self.width = width
        self.height = height

        self.c.create_text(width / 2.0, height / 2.0, font=("Arial", size, ''), fill="white", text=text)

    def getWidget(self):
        return self.c