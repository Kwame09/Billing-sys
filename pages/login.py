from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from pages.mainlayout import MainLayoutPage
from common import authenticate, session

class LoginPage():
    '''
    Login Page
    '''

    def __init__(self, window, x: float, y: float):
        self.window = window
        self.positionX = x 
        self.positionY = y
        #self.initialize()
    
    def initialize(self):
        '''
        Initialize Page Contents
        '''

        width = 400
        height = 500

        positionY = self.positionY-(height/3.5)

        self.window.geometry("%dx%d+%d+%d"%(width, height, self.positionX,positionY))
        self.window.title('LOGIN - Supermarket Billing System')
        self.frame = Frame(
            self.window,
            width=400,
            height=450
        )

        self.create_content()
        self.frame.place(anchor="c", relx=0.5, rely=0.5)
    
    def create_content(self):
        '''
        Create Login Page Components
        '''
        
        ttk.Label(
            self.frame,
            text='Login Page',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)
        
        ttk.Label(
            self.frame,
            text='Login As',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.3)

        self.role_var = StringVar()
        self.role_var.set('cashier')
        role_select = ttk.Combobox(
            self.frame,
            textvariable=self.role_var,
            font='monospace 10',
            foreground='#4e4e4e',
            background='white',
            values=('cashier', 'admin'),
            state='readonly',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.36)

        ttk.Label(
            self.frame,
            text='Username',
            font='sans-serif 11',
            foreground="#242424",
            justify='center'
        ).place(anchor='c', relx=0.5, rely=0.46)

        self.username_var = StringVar()
        ttk.Entry(
            self.frame,
            textvariable=self.username_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.52)

        ttk.Label(
            self.frame,
            text='Password',
            font='sans-serif 11',
            foreground="#242424",
            justify='center'
        ).place(anchor='c', relx=0.5, rely=0.63)

        self.password_var = StringVar()
        ttk.Entry(
            self.frame,
            textvariable=self.password_var,
            foreground='#4e4e4e',
            font='monospace 10',
            show='*',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.69)

        Button(
            self.frame,
            text='LOGIN',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.authenticate
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.8)

        self.mainlayout = MainLayoutPage(self.window, self.positionX, self.positionY)
    
    def authenticate(self):
        global session

        if not self.mainlayout.is_initialized:
            user = authenticate(self.username_var.get(), self.password_var.get(), self.role_var.get())
            if user:
                session['user'] = user
                self.mainlayout.initialize()
            else:
                messagebox.showerror('Error', 'Invalid login credentials!!!')