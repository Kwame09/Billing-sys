from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkcalendar import Calendar

import os
from datetime import datetime

from models import Product
from common import session


class BSCalendar(Toplevel):
    '''
    Calendar Window
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.title('Calendar')
        self.geometry("250x200")
        self.selected_date = StringVar()
        self.content()

    def content(self):
        today = datetime.utcnow()
        self.selected_date.set(f"{today.year}")
        self.calendar = Calendar(self, year=today.year, month=today.month, day=today.day, selectmode='day', borderwidth=0, showothermonthdays=False, textvariable=self.selected_date)
        self.calendar.pack(anchor='c', side='top', fill='both', expand=True)

        Button(
            self,
            text='Filter',
            font='monospace 10',
            command=self.destroy
        ).pack(anchor='se', side='top')
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        if self.selected_date.get():
            return self.selected_date.get()
        return self.calendar.get_displayed_month() 
        
        #self.mainloop()
    