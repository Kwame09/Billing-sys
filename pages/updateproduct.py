from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os

from models import Product
from common import session


class UpdateProductPage(Toplevel):
    '''
    New Product Form Window
    '''

    def __init__(self, product, master=None, **kw):
        super().__init__(master, **kw)
        self.product = product
        self.title('Update Product')
        self.geometry("400x500")
        self.updated_product = None
        self.content()
        self.get_product()
    
    def get_product(self):
        self.product_name_var.set(self.product.name)
        self.product_price_var.set(self.product.price)
        self.product_quantity_var.set(self.product.quantity)
    
    def update_product(self):
        '''
        Function for committing update
        to database

        @params None
        @return None
        '''
        update = {'name': self.product_name_var.get(), 
                'price': self.product_price_var.get(), 
                'image': '',
                'quantity': self.product_quantity_var.get()}

        result = Product.update(self.product.id, update)
        
        if result.isnumeric():
            product = (self.product.id, update['name'],
                update['price'], update['quantity'])
            
            self.updated_product = product
        else:
            messagebox.showerror('Error Message', result['message'])
        self.destroy()
    

    def content(self):
        #const_url = "add_img.png"
        #img_url = os.path.realpath(os.path.join(os.curdir, 'assets', const_url))
        #add_img = ImageTk.PhotoImage(Image.open(img_url).resize((60, 50)))

        ttk.Label(
            self,
            text='Update Product',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)

        Button(
            self,
            text='Product Image Here',
            #image=add_img,
            compound='top',
            font='Arial 11'
        ).place(anchor='c', width=250, height=80, relx=0.5, rely=0.3)

        ttk.Label(
            self,
            text='Product Name',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.42)

        self.product_name_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.product_name_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.48)

        ttk.Label(
            self,
            text='Product Price',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.56)

        self.product_price_var = DoubleVar()
        ttk.Entry(
            self,
            textvariable=self.product_price_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.62)

        ttk.Label(
            self,
            text='Product Quantity',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.7)

        self.product_quantity_var = IntVar()
        ttk.Entry(
            self,
            textvariable=self.product_quantity_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.76)

        Button(
            self,
            text='Update',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.update_product,
            state='normal' if session.user.is_admin() else 'disabled'
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.86)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.updated_product
        
        #self.mainloop()
    