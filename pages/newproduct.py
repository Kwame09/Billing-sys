from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os
from datetime import datetime

from models import Product
from assets import AddImageIcon


class AddProductPage(Toplevel):
    '''
    New Product Form Window
    '''

    def __init__(self, master=None, **kw):
        super().__init__()
        self.title('Add Product')
        self.geometry("400x500")
        self.new_product = None
        self.content()
    
    def add_product(self):
        'Items, Price, Item_image_link, Quantity'
        new_product = {'name': self.new_product_name_var.get(), 
                'price': self.new_product_price_var.get(), 
                'image': '',
                'quantity': self.new_product_quantity_var.get()}
        
        product = Product(**new_product)
        result = product.save()
        
        if result.isnumeric():
            self.new_product = Product.get(result)
        else:
            messagebox.showerror('Error Message', result['message'])
        self.destroy()
    

    def content(self):
        #add_img = ImageTk.PhotoImage(AddImageIcon.resize((50, 50)))
        
        ttk.Label(
            self,
            text='Add Product',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)

        Button(
            self,
            text='Product Image',
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

        self.new_product_name_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.new_product_name_var,
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

        self.new_product_price_var = DoubleVar()
        ttk.Entry(
            self,
            textvariable=self.new_product_price_var,
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

        self.new_product_quantity_var = IntVar()
        ttk.Entry(
            self,
            textvariable=self.new_product_quantity_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.76)

        Button(
            self,
            text='Save',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.add_product
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.86)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.new_product
        
        #self.mainloop()
    