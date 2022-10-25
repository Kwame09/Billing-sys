from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os
from common.utils import Utils

from models import User
from common import session


class UpdateUserPage(Toplevel):
    '''
    New User Form Window
    '''

    def __init__(self, user, master=None, **kw):
        super().__init__(master, **kw)
        self.user = user
        self.title('Update User')
        self.geometry("400x500")
        self.updated_user = None
        self.content()
        self.get_user()
    
    def get_user(self):
        self.user_name_var.set(self.user.name)
        self.user_username_var.set(self.user.username)
        self.user_role_var.set(self.user.role)
    
    def update_user(self):
        '''
        Function for committing update
        to database

        @params None
        @return None
        '''
        update = {'username': self.user_username_var.get(), 
                'name': self.user_name_var.get(), 
                'role': self.user_role_var.get()}
        
        if len(self.user_password_var.get()):
            update['password'] = Utils.hash_password(self.user_password_var.get())

        result = User.update(self.user.id, update)
        
        if result.isnumeric():
            user = User.get(self.user.id)
            update = (self.user.id, user.username,
                user.name, user.role, user.updated_at)
            
            self.updated_user = update
        else:
            messagebox.showerror('Error Message', result['message'])
        self.destroy()
    

    def content(self):
        '''
        Update user details
        '''

        ttk.Label(
            self,
            text='Update User',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)

        ttk.Label(
            self,
            text='Role',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.3)

        self.user_role_var = StringVar()
        self.user_role_var.set(self.user.role)
        ttk.Combobox(
            self,
            textvariable=self.user_role_var,
            font='monospace 10',
            foreground='#4e4e4e',
            background='white',
            values=('cashier', 'admin'),
            state='readonly',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.36)

        ttk.Label(
            self,
            text='Full Name',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.46)

        self.user_name_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.user_name_var,
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

        self.user_username_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.user_username_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.66)

        ttk.Label(
            self,
            text='New Password',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.74)

        self.user_password_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.user_password_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center',
            show='*'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.80)

        Button(
            self,
            text='Update',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.update_user,
            state='normal' if session.user.is_admin() else 'disabled'
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.90)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.updated_user
        
        #self.mainloop()
    