from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk

from models import Sale
from models import User
from pages import LabelPage
from pages.calendar import BSCalendar as Calendar
from pages.newsale import AddSalePage
from pages.updatesale import UpdateSalePage
from assets import AddImageIcon
from common import session

from datetime import datetime, timedelta

class SalesPage(LabelPage):
    '''
    Sales List Page
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.sales_list = [Sale(**sale) for sale in Sale.order_by('updated_at').get()]

    def update_sales_table(self, sale):
        self.sales_table.insert(parent='', index=0, iid=sale[0], text='',
                                    values=sale)
    
    def populate_sales_table(self, event=None):
        filtered = self.filter_var.get().lower()
        days_to_num_in_week = {
            'Sun': 0,
            'Mon': 1,
            'Tue': 2,
            'Wed': 3,
            'Thu': 4,
            'Fri': 5,
            'Sat': 6
        }
        if filtered == 'today':
            today = datetime.utcnow()
            date = datetime(today.year, today.month, today.day).strftime("%Y-%m-%d %H:%M:%S")
            query = f"created_at >= '{date}'"
            sales = [Sale(**sale) for sale in  Sale.where(query).order_by('updated_at').get()]
        
        elif filtered == 'this week':
            today = datetime.utcnow()
            num_of_days = days_to_num_in_week[today.strftime("%a")]
            week = today - timedelta(days=num_of_days)
            date = datetime(week.year, week.month, week.day).strftime("%Y-%m-%d %H:%M:%S")
            query = f"created_at >= '{date}'"
            sales = [Sale(**sale) for sale in  Sale.where(query).order_by('updated_at').get()]
        
        elif filtered == 'this month':
            today = datetime.utcnow()
            date = datetime(today.year, today.month, 1).strftime("%Y-%m-%d %H:%M:%S")
            query = f"created_at >= '{date}'"
            sales = [Sale(**sale) for sale in  Sale.where(query).order_by('updated_at').get()]
            
        elif self.filter_var.get().lower() == 'custom':
            calendar_window = Calendar(
                self.master
            )
            result = calendar_window.show()
            
            if type(result) is tuple:
                custom_date = datetime(result[1], result[0], 1)
                date = custom_date.strftime("%Y-%m-%d %H:%M:%S")
                query = f"created_at >= '{date}'"
                
                self.filter_var.set(custom_date.strftime("%b %Y"))
            else:
                date_str = result.split('/')
                start_date = datetime(int(f'20{date_str[2]}'), int(date_str[0]), int(date_str[1]))
                self.filter_var.set(start_date.strftime("%a %b %d %Y"))
                end_date = start_date + timedelta(days=1)
                start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
                end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
                query = f"created_at BETWEEN '{start_date}' AND '{end_date}'"
 
            sales = [Sale(**sale) for sale in  Sale.where(query).order_by('updated_at').get()]

        else:
            sales = [Sale(**sale) for sale in Sale.order_by('updated_at').get()]
        
        self.sales_list = sales

        for item in self.sales_table.get_children():
            self.sales_table.delete(item)

        if type(self.sales_list) is list:
            self.update_sales_count()
            self.update_sales_total()
            for sale in self.sales_list:
                sale = sale.json()
                self.update_sales_table((sale['id'],sale['salesperson']['username'], sale['count'], 
                                         sale['total'], sale['updated_at']))
        else:
            print(self.sales_list)
        
    def update_sales_count(self):
        self.sales_count['text'] = str(Sale.count())
    
    def update_sales_total(self):
        self.sales_total.set(Sale.sum('total'))
    
    def add_sale_window(self):
        sale_window = AddSalePage(
            self.master
        )
        sale = sale_window.show()
        if sale:
            self.sales_list.append(sale)
            self.update_sales_count()
            self.update_sales_total()
            sale = sale.json()
            self.update_sales_table((sale['id'],sale['salesperson']['username'], sale['count'], 
                                         sale['total'], sale['updated_at']))
    
    def update_sale_window(self, event=None):
        if len(self.sales_table.selection()):
            selected = self.sales_table.item(self.sales_table.selection()[0])
            
            sale = Sale.get(selected['values'][0])

            sale_window = UpdateSalePage(
                sale,
                self.master
            )
            
            result = sale_window.show()
            
            if result:
                self.update_sales_total()
                self.sales_table.item(self.sales_table.selection()[0], text='', values=result)
        else:
            messagebox.showwarning('Error Message', 'Select a row to update')
    
    def delete_sale(self):
        if len(self.sales_table.selection()):
            selected = self.sales_table.item(self.sales_table.selection()[0])
            
            confirm = messagebox.askyesno(
                title='Deletion Confirmation',
                message='Delete this sale?'
            )
            if confirm:
                result = Sale.delete(selected['values'][0])
                if result:
                    self.sales_table.delete(self.sales_table.selection()[0])
                    self.update_sales_count()
                    self.update_sales_total()
        else:
            messagebox.showwarning('Error Message', 'Select a row to delete')

    def content(self):
        ''''
        Create sales page components
        '''
        plus_img = ImageTk.PhotoImage(AddImageIcon.resize((50, 50)))

        tools_frame = ttk.Frame(
            self
        )

        sales_frame = ttk.Frame(
            self
        )

        sales_card = ttk.Frame(
            tools_frame
        )

        ttk.Label(
            sales_card,
            text='Sales',
            image=self.assets['sales'],
            compound='top',
            font='Helvetica 15',
            foreground='#4f4f4f',
            borderwidth=2
        ).grid(column=0, row=0)

        self.sales_count = ttk.Label(
            sales_card,
            text='0',
            foreground='gray',
            font='monospace 50',
        )
        self.sales_count.grid(column=1, row=0, padx=10)

        sales_card.grid(column=0, row=0, sticky='nw')

        self.sales_total = DoubleVar()
        self.sales_total.set(0.00)
        ttk.Label(
            tools_frame,
            textvariable=self.sales_total,
            foreground='brown',
            font='Arial 30',
        ).grid(column=5, row=0, padx=10, sticky='e')

        self.filter_var = StringVar()
        self.filter_var.set('All')
        filterbox = ttk.Combobox(
            tools_frame,
            textvariable=self.filter_var,
            font='monospace 10',
            foreground='#4e4e4e',
            background='white',
            values=('All', 'Today', 'This Week', 'This Month', 'Custom'),
            state='readonly',
            justify='center'
        )
        filterbox.bind("<<ComboboxSelected>>", self.populate_sales_table)
        filterbox.grid(column=0, row=1, ipady=5)

        Button(
            tools_frame,
            text='Add Sale',
            command=self.add_sale_window
        ).grid(column=1, row=1, padx=10)

        Button(
            tools_frame,
            text='Sale Details',
            command=self.update_sale_window
        ).grid(column=2, row=1, padx=10)

        Button(
            tools_frame,
            text='Delete Sale',
            command=self.delete_sale
        ).grid(column=3, row=1, padx=10)

        tools_frame.grid(column=0, row=1, padx=10, pady=5, sticky='nw')

        self.sales_table = ttk.Treeview(sales_frame, height=14)
        self.sales_table['columns'] = ('item_id', 'salesperson', 'count', 
                                       'total', 'date')
        self.sales_table.column('#0', width=0, stretch=NO)
        self.sales_table.column('item_id', width=0, stretch=NO)
        self.sales_table.column('salesperson', anchor=CENTER)
        self.sales_table.column('count', anchor=CENTER)
        self.sales_table.column('total', anchor=CENTER)
        self.sales_table.column('date', anchor=CENTER)

        self.sales_table.heading('#0', text='', anchor=CENTER)
        self.sales_table.heading('item_id', text='', anchor=CENTER)
        self.sales_table.heading('salesperson', text='Sold By', anchor=CENTER)
        self.sales_table.heading('count', text='Items Count', anchor=CENTER)
        self.sales_table.heading('total', text='Total', anchor=CENTER)
        self.sales_table.heading('date', text='Date', anchor=CENTER)

        #self.sales_table.bind("<<TreeviewSelect>>", self.update_sale_window)
        self.sales_table.grid(column=0, row=0, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(sales_frame, orient='vertical', command=self.sales_table.yview)
        self.sales_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky='ns')

        sales_frame.grid(column=0, row=2, pady=5, padx=10, sticky='s')

        self.after(5, self.populate_sales_table)

    