from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os
from datetime import datetime

from models import User
from assets import AddImageIcon


class AddUserPage(Toplevel):
    '''
    New User Form Window
    '''

    def __init__(self, master=None, **kw):
        super().__init__()
        self.title('Add User')
        self.geometry("400x500")
        self.new_user = None
        self.content()
    
    def add_user(self):
        new_user = {'username': self.new_user_username_var.get(), 
                    'name': self.new_user_name_var.get(), 
                    'role': self.new_user_role_var.get(),
                    'password': self.new_user_password_var.get()}
        
        user = User(**new_user)
        result = user.add()
        
        if result.isnumeric():
            self.new_user = User.get(result)
        else:
            messagebox.showerror('Error Message', result['message'])
        self.destroy()
    

    def content(self):
        #add_img = ImageTk.PhotoImage(AddImageIcon.resize((50, 50)))
        
        ttk.Label(
            self,
            text='Add User',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)

        ttk.Label(
            self,
            text='Role',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.3)

        self.new_user_role_var = StringVar()
        self.new_user_role_var.set('cashier')
        ttk.Combobox(
            self,
            textvariable=self.new_user_role_var,
            font='monospace 10',
            foreground='#4e4e4e',
            background='white',
            values=('cashier', 'administrator'),
            state='readonly',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.36)

        ttk.Label(
            self,
            text='Full Name',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.46)

        self.new_user_name_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.new_user_name_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.52)

        ttk.Label(
            self,
            text='Username',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.60)

        self.new_user_username_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.new_user_username_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.66)

        ttk.Label(
            self,
            text='Password',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.74)

        self.new_user_password_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.new_user_password_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center',
            show='*'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.80)

        Button(
            self,
            text='Save',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.add_user
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.90)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.new_user
        
        #self.mainloop()
    