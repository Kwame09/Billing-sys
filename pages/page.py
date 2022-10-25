from tkinter import ttk
from cairosvg import svg2png
from PIL import ImageTk, Image

from io import BytesIO
import os

from assets import ChartAreaIcon, ShoppingCartIcon, ShoppingBasketIcon,\
                    UsersIcon, ChartPieIcon, PlusIcon

class Page(ttk.Frame):
    '''
    Initial Class for Pages Frame.
    Inherits from ttk.Frame
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.build_assets
        self.content()

    def build_assets(self):
        self.assets = {
            'dashboard'  : ImageTk.PhotoImage(ChartAreaIcon.resize((50, 50))),
            'sales'      : ImageTk.PhotoImage(ShoppingCartIcon.resize((50, 50))),
            'products'   : ImageTk.PhotoImage(ShoppingBasketIcon.resize((50, 50))),
            'users'      : ImageTk.PhotoImage(UsersIcon.resize((50, 50))),
            'settings'   : ImageTk.PhotoImage(ChartPieIcon.resize((50, 50))),
            'addButton'  : ImageTk.PhotoImage(PlusIcon.resize((50, 50)))}
        
    def content(self):
        pass

class LabelPage(ttk.LabelFrame):
    '''
    Initial Class for Pages Frame.
    Inherits from ttk.Frame
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.build_assets()
        self.content()

    def build_assets(self):
        self.assets = {
            'dashboard'  : ImageTk.PhotoImage(ChartAreaIcon.resize((50, 50))),
            'sales'      : ImageTk.PhotoImage(ShoppingCartIcon.resize((50, 50))),
            'products'   : ImageTk.PhotoImage(ShoppingBasketIcon.resize((50, 50))),
            'users'      : ImageTk.PhotoImage(UsersIcon.resize((50, 50))),
            'settings'   : ImageTk.PhotoImage(ChartPieIcon.resize((50, 50))),
            'addButton'  : ImageTk.PhotoImage(PlusIcon.resize((50, 50)))}

    def content(self):
        pass