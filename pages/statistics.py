from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk

from models import User
from models import Sale
from models import SaleItem
from models import Product
from pages import LabelPage

from common import session

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

class StatisticsPage(LabelPage):
    '''
    Statistics List Page
    '''

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.filter = None
    
    def set_filter(self, event=None):
        self.filter = self.filter_var.get().lower()
        self.draw_charts()

    def draw_charts(self, event=None):
        sales_per_product = SaleItem.select('product_id, SUM(quantity) AS quantity, SUM(total) AS total').group_by(1).order_by(3, 'desc').get()
        sales_per_person = Sale.select('user_id, COUNT(*) AS count, SUM(TOTAL) AS total').group_by('user_id').get()
        for item in sales_per_person:
            user = User.get(item['user_id'])
            item['user'] = user.name
            print(item)
        print("================================")

        data = {'Products': [], 'Sales': []}
        for item in sales_per_product:
            # sale = Sale.get(item['sales_id'])
            # item['seller'] = sale.salesperson()['name']
            product = Product.get(item['product_id'])
            item['product'] = product.name

            data['Products'].append(item['product'])
            data['Sales'].append(float(item['quantity']))
            print(item)

        df1 = DataFrame(data, columns=['Products', 'Sales'])
        
        figure = plt.figure(figsize=(7,3.3), dpi=100)
        ax1 = figure.add_subplot(111)
        self.chart_figure = FigureCanvasTkAgg(figure, self.charts_frame)
        self.chart_figure.get_tk_widget().grid(row=0, column=0)
        df1 = df1[['Products', 'Sales']].groupby('Products').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_xlabel('Products')
        ax1.set_ylabel('Sales')
        ax1.set_title('Sales Per Product')

    def content(self):
        ''''
        Create page components

        @params None
        @return None
        '''

        tools_frame = ttk.Frame(
            self
        )

        self.charts_frame = ttk.Frame(
            self
        )

        info_card = ttk.Frame(
            tools_frame
        )

        ttk.Label(
            info_card,
            text='Statistics',
            image=self.assets['settings'],
            compound='left',
            font='Helvetica 15',
            foreground='#4f4f4f',
            borderwidth=2
        ).grid(column=0, row=0)

        self.misc_text = ttk.Label(
            info_card,
            text='',
            foreground='gray',
            font='monospace 30',
        )
        self.misc_text.grid(column=1, row=0, padx=10)

        info_card.grid(column=0, row=0, sticky='nw')

        self.filter_var = StringVar()
        self.filter_var.set('Cashier')
        values = ['Cashier']
        if session.user.is_admin() is True:
            self.filter_var.set('All')
            values.insert(0, 'All')
            values.append('Admin')

        rolecombo = ttk.Combobox(
            tools_frame,
            textvariable=self.filter_var,
            font='Helvetica 10',
            foreground='#4e4e4e',
            background='white',
            values=values,
            state='readonly',
            justify='center'
        )
        if session.user.is_admin() is True:
            rolecombo.bind('<<ComboboxSelected>>', self.set_filter)
        rolecombo.grid(column=0, row=1, ipady=5)

        # if session.user.is_admin() is True:
        #     Button(
        #         tools_frame,
        #         text='Add Sale',
        #         command=self.add_user_window
        #     ).grid(column=1, row=1, padx=10)

        #     Button(
        #         tools_frame,
        #         text='Sale Details',
        #         command=self.update_user_window
        #     ).grid(column=2, row=1, padx=10)

        #     Button(
        #         tools_frame,
        #         text='Delete Sale',
        #         command=self.delete_user
        #     ).grid(column=3, row=1, padx=10)

        tools_frame.grid(column=0, row=2, padx=10, pady=5, sticky='nw')

        self.draw_charts()
        #self.bind('<<OnPacked>>', self.draw_charts)
        self.charts_frame.grid(column=0, row=3, pady=5, padx=10, sticky='s')
    
        self.master.wm_protocol('WM_DELETE_WINDOW', self.exit)

    def exit(self):
        self.chart_figure.stop_event_loop()