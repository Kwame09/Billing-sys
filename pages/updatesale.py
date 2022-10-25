from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os

from models import Sale
from models import Product
from assets import AddImageIcon
from models import SaleItem

from pages.newsaleitem import AddSaleItemPage


class UpdateSalePage(Toplevel):
    '''
    New Sale Form Window
    '''

    def __init__(self, sale, master=None, **kw):
        super().__init__(master, **kw)
        self.sale = sale
        self.title('Update Sale')
        self.geometry("600x510")
        self.updated_sale = None
        self.saleitems = []
        self.content()
        self.get_saleitems()
    
    def get_saleitems(self):
        saleitems = SaleItem.find({'sales_id': self.sale.id})
        for item in saleitems:
            item = item.json()

            sale_item = (item['id'], item['product'], item['quantity'], item['total'])
            self.update_saleitems_table(sale_item)
    
    def update_products_table(self, product):
        self.products_table.insert(parent='', index=0, iid=product[0], text='',
                                    values=product)
    
    def update_saleitems_table(self, product):
        self.saleitems_table.insert(parent='', index=0, iid=product[0], text='',
                                    values=product)

    def open_saleitem_window(self, event):
        if (self.products_table.selection()):
            selected = self.products_table.item(self.products_table.selection()[0])
            
            product = Product.get(selected['values'][0])
            
            saleitem_window = AddSaleItemPage(
                product,
                self
            )
        
            result = saleitem_window.show()
            if result:
                self.saleitems.append(result)
                self.update_saleitems_table(result)

    def search_products(self, event):
        if len(self.product_search_var.get()) > 1:
            for item in self.products_table.get_children():
                self.products_table.delete(item)

            products = Product.search('name', self.product_search_var.get())
            for product in products:
                self.update_products_table((product.id, product.name,
                 product.price, product.quantity))
    
    def update_sale(self):
        total = 0
        for item in self.saleitems_table.get_children():
            item = self.saleitems_table.item(item)['values']
            total += float(item[-1])
        update = {'total': total}
        
        sale_id = Sale.update(self.sale.id, update)
        
        if sale_id.isnumeric():
            for item in self.saleitems:
                saleitem = SaleItem(self.sale.id, item[0], item[2], item[3])
                saleitem.save()

            sale = Sale.get(self.sale.id)
            sale = sale.json()

            self.updated_sale = (sale['id'],sale['salesperson']['username'], sale['count'], 
                            sale['total'], sale['updated_at'])

        self.destroy()

    def content(self):
        #add_img = ImageTk.PhotoImage(AddImageIcon.resize((50, 50)))
        tools_frame = Frame(
            self
        )
        
        ttk.Label(
            self,
            text='Update Sale',
            font='Helvetica 20 bold',
            foreground='#da1039'
        ).pack(anchor='c', side='top', pady=5)


        self.product_search_var = StringVar()
        self.product_search_var.set('Product Search')
        self.product_search_entry = ttk.Entry(
            tools_frame,
            textvariable=self.product_search_var,
            foreground='#4e4e4e',
            font='monospace 10',
            justify='center',
            width=25
        )
        self.product_search_entry.bind('<FocusIn>', lambda ev: self.product_search_var.set(''))
        self.product_search_entry.bind('<KeyRelease>', self.search_products)
        self.product_search_entry.pack(ipady=5)
        
        tools_frame.pack(side='top', anchor='ne', padx=15, pady=10)

        self.products_table = self.create_products_search_table()
        self.products_table.pack(anchor='center', side="top", padx=15, pady=0.12)

        ttk.Label(
            self,
            text='Selected Items',
            font='Arial 11 bold',
            foreground="#242424"
        ).pack(pady=10, padx=15, anchor='w')

        self.saleitems_table = self.create_saleitems_table()
        self.saleitems_table.pack(anchor='center', side="top", padx=15, pady=0.12)

        Button(
            self,
            text='Update',
            background='#0052ea',
            activebackground='#0052ea',
            foreground='white',
            activeforeground='white',
            font='monospace 13 bold',
            command=self.update_sale
        ).pack(side='right', padx=15)
    
    def create_products_search_table(self):
        products_table = ttk.Treeview(self, height=5)
        products_table['columns'] = ('item_id', 'item_name', 'item_price',
                                     'item_quantity')
        products_table.column('#0', width=0, stretch=NO)
        products_table.column('item_id', width=0, stretch=NO)
        products_table.column('item_name', anchor=CENTER)
        products_table.column('item_price', anchor=CENTER)
        products_table.column('item_quantity', anchor=CENTER)

        products_table.heading('#0', text='', anchor=CENTER)
        products_table.heading('item_id', text='', anchor=CENTER)
        products_table.heading('item_name', text='Name', anchor=CENTER)
        products_table.heading('item_price', text='Price', anchor=CENTER)
        products_table.heading('item_quantity', text='In Stock', anchor=CENTER)

        products_table.bind("<<TreeviewSelect>>", self.open_saleitem_window)
        return products_table
    
    def create_saleitems_table(self):
        saleitems_table = ttk.Treeview(self)
        saleitems_table['columns'] = ('item_id', 'item_name', 'item_quantity',
                                     'item_total')
        saleitems_table.column('#0', width=0, stretch=NO)
        saleitems_table.column('item_id', width=0, stretch=NO)
        saleitems_table.column('item_name', anchor=CENTER)
        saleitems_table.column('item_quantity', anchor=CENTER)
        saleitems_table.column('item_total', anchor=CENTER)

        saleitems_table.heading('#0', text='', anchor=CENTER)
        saleitems_table.heading('item_id', text='', anchor=CENTER)
        saleitems_table.heading('item_name', text='Name', anchor=CENTER)
        saleitems_table.heading('item_quantity', text='Quantity', anchor=CENTER)
        saleitems_table.heading('item_total', text='Total Price', anchor=CENTER)

        #saleitems_table.bind("<<TreeviewSelect>>", self.update_product)
        return saleitems_table
        
    
    def show(self):
        self.deiconify()
        self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        return self.updated_sale
        
        #self.mainloop()
    