from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os

from models import Sale
from models import saleitem
from models import Product

class AddSaleItemPage(Toplevel):
    '''
    New SaleItem Form Window
    '''

    def __init__(self, product, master=None, **kw):
        super().__init__()
        self.product = product
        self.title('Add Sales Item')
        self.geometry("400x500")
        self.saleitem = None
        self.content()
        self.get_product()
    
    def get_product(self):
        self.product_name_var.set(self.product.name)
        self.product_quantity_var.set(1)
        self.product_total_var.set(self.product.price)
    
    def update_total(self, event):
        try:
            quantity = self.product_quantity_var.get()
            self.product_total_var.set(self.product.price*quantity)
        except: 
            pass
    
    def add_saleitem(self):
        self.saleitem = (
            self.product.id,
            self.product.name,
            self.product_quantity_var.get(),
            self.product_total_var.get()
        )
        self.destroy()

    def content(self):
        #const_url = "add_img.png"
        #img_url = os.path.realpath(os.path.join(os.curdir, 'assets', const_url))
        #add_img = ImageTk.PhotoImage(Image.open(img_url).resize((60, 50)))

        ttk.Label(
            self,
            text='Add Item',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).place(anchor='c', relx=0.5, rely=0.15)

        ttk.Label(
            self,
            text='Item Name',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.3)

        self.product_name_var = StringVar()
        ttk.Entry(
            self,
            textvariable=self.product_name_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center',
            state='readonly'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.36)

        ttk.Label(
            self,
            text='Item Price',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.46)

        self.product_total_var = DoubleVar()
        ttk.Entry(
            self,
            textvariable=self.product_total_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center',
            state='readonly'
        ).place(anchor='c', width=250, height=35, relx=0.5, rely=0.52)

        ttk.Label(
            self,
            text='Item Quantity',
            font='sans-serif 11',
            foreground="#242424"
        ).place(anchor='c', relx=0.5, rely=0.62)

        self.product_quantity_var = IntVar()
        quantity_enty = ttk.Entry(
            self,
            textvariable=self.product_quantity_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center'
        )
        quantity_enty.bind('<KeyRelease>', self.update_total)
        quantity_enty.place(anchor='c', width=250, height=35, relx=0.5, rely=0.68)

        Button(
            self,
            text='Add',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.add_saleitem
        ).place(anchor='c', width=250, height=45, relx=0.5, rely=0.8)
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.saleitem
        
        #self.mainloop()
    