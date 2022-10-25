from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk

from models import User
from pages import LabelPage
from pages.newuser import AddUserPage
from pages.updateuser import UpdateUserPage
from assets import AddImageIcon

from common import session

class UsersPage(LabelPage):
    '''
    Users List Page
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.filter = None
    
    def set_filter(self, event=None):
        self.filter = self.filter_var.get().lower()
        self.populate_users_table()

    def update_users_table(self, user):
        self.users_table.insert(parent='', index=0, iid=user[0], text='',
                                    values=user)
    
    def populate_users_table(self):
        for item in self.users_table.get_children():
                self.users_table.delete(item)
        if self.filter is not None and self.filter != 'all':
            self.users_list = User.find({'role': self.filter})
        elif session.user.is_admin() is True or self.filter == 'all':
            self.users_list = User.all()
        else:
            self.users_list = User.find({'role': 'cashier'})
        
        if type(self.users_list) is list:
            self.update_users_count()
            
            for user in self.users_list:
                self.update_users_table((user.id, user.username, user.name, 
                                         user.role, user.updated_at))
                
        else:
            print(self.users_list)
        
    def update_users_count(self):
        if self.filter is not None and self.filter != 'all':
            self.users_count['text'] = str(User.count({'role': self.filter}))
        elif session.user.is_admin() is True or self.filter == 'all':
            self.users_count['text'] = str(User.count())
        else:
            self.users_count['text'] = str(User.count({'role': 'cashier'}))
    
    def add_user_window(self):
        user_window = AddUserPage(
            self.master
        )
        user = user_window.show()
        if user:
            self.update_users_count()
            self.update_users_table((user.id, user.username, user.name,
                             user.role, user.updated_at))
    
    def update_user_window(self, event=None):
        if len(self.users_table.selection()):
            selected = self.users_table.item(self.users_table.selection()[0])
            
            user = User.get(selected['values'][0])
            
            user_window = UpdateUserPage(
                user,
                self.master
            )
            
            result = user_window.show()
            
            if result:
                self.users_table.item(self.users_table.selection()[0], text='', values=result)
        else:
            messagebox.showwarning('Error Message', 'Select a row to update')
    
    def delete_user(self):
        if len(self.users_table.selection()):
            selected = self.users_table.item(self.users_table.selection()[0])
            
            confirm = messagebox.askyesno(
                title='Deletion Confirmation',
                message='Delete this user?'
            )
            if confirm:
                result = User.delete(selected['values'][0])
                if result:
                    self.users_table.delete(self.users_table.selection()[0])
                    self.update_users_count()
        else:
            messagebox.showwarning('Error Message', 'Select a row to delete')
    
    def content(self):
        ''''
        Create users page components
        '''
        plus_img = ImageTk.PhotoImage(AddImageIcon.resize((50, 50)))

        tools_frame = ttk.Frame(
            self
        )

        users_frame = ttk.Frame(
            self
        )

        users_card = ttk.Frame(
            tools_frame
        )

        ttk.Label(
            users_card,
            text='Users',
            image=self.assets['users'],
            compound='top',
            font='Helvetica 15',
            foreground='#4f4f4f',
            borderwidth=2
        ).grid(column=0, row=0)

        self.users_count = ttk.Label(
            users_card,
            text='0',
            foreground='gray',
            font='monospace 50',
        )
        self.users_count.grid(column=1, row=0, padx=10)

        users_card.grid(column=0, row=0, sticky='nw')

        self.filter_var = StringVar()
        self.filter_var.set('Cashier')
        values = ['Cashier']
        if session.user.is_admin() is True:
            self.filter_var.set('All')
            values.insert(0, 'All')
            values.append('Admin')

        rolecombo =ttk.Combobox(
            tools_frame,
            textvariable=self.filter_var,
            font='monospace 10',
            foreground='#4e4e4e',
            background='white',
            values=values,
            state='readonly',
            justify='center'
        )
        if session.user.is_admin() is True:
            rolecombo.bind('<<ComboboxSelected>>', self.set_filter)
        rolecombo.grid(column=0, row=1, ipady=5)

        if session.user.is_admin() is True:
            Button(
                tools_frame,
                text='Add User',
                command=self.add_user_window
            ).grid(column=1, row=1, padx=10)

            Button(
                tools_frame,
                text='User Details',
                command=self.update_user_window
            ).grid(column=2, row=1, padx=10)

            Button(
                tools_frame,
                text='Delete User',
                command=self.delete_user
            ).grid(column=3, row=1, padx=10)

        tools_frame.grid(column=0, row=1, padx=10, pady=5, sticky='nw')

        self.users_table = ttk.Treeview(users_frame, height=14)
        self.users_table['columns'] = ('user_id', 'username', 'name',
                                       'role', 'date')
        self.users_table.column('#0', width=0, stretch=NO)
        self.users_table.column('user_id', width=0, stretch=NO)
        self.users_table.column('username', anchor=CENTER)
        self.users_table.column('name', anchor=CENTER)
        self.users_table.column('role', anchor=CENTER)
        self.users_table.column('date', anchor=CENTER)

        self.users_table.heading('#0', text='', anchor=CENTER)
        self.users_table.heading('user_id', text='', anchor=CENTER)
        self.users_table.heading('username', text='Username', anchor=CENTER)
        self.users_table.heading('name', text='Full Name', anchor=CENTER)
        self.users_table.heading('role', text='Role', anchor=CENTER)
        self.users_table.heading('date', text='Date', anchor=CENTER)

        #self.users_table.bind("<<TreeviewSelect>>", self.update_user_window)
        self.users_table.grid(column=0, row=0, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(users_frame, orient='vertical', command=self.users_table.yview)
        self.users_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        users_frame.grid(column=0, row=2, pady=5, padx=10, sticky='s')

        self.after(5, self.populate_users_table)

    