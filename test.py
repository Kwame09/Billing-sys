from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk

from models import Sale
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

    def draw_charts(self):
        data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                 'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]}
        df1 = DataFrame(data1, columns=['Country', 'GDP_Per_Capita'])

        data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
                 'Unemployment_Rate': [9.8, 12,8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]}
        df2 = DataFrame(data2, columns=['Year', 'Unemployment_Rate'])

        data3 = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
                 'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]}
        df3 = DataFrame(data3, columns=['Interest_Rate', 'Stock_Index_Price'])

        figure1 = plt.figure(figsize=(3,2), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.charts_frame)
        bar1.get_tk_widget().grid(row=0, column=0)
        df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

        figure2 = plt.figure(figsize=(3,2), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self.charts_frame)
        line2.get_tk_widget().grid(row=1, column=2)
        df2 = df2[['Year', 'Unemployment_Rage']].groupby('Year').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        ax2.set_title('Year Vs. Unemployment Rate')

        figure3 = plt.figure(figsize=(3,2), dpi=100)
        ax3 = figure3.add_subplot(111)
        ax3.scatter(df3['Interest_Rate'], df3['Stock_Index_Price'], color='g')
        scatter3 = FigureCanvasTkAgg(figure3, self.charts_frame)
        scatter3.get_tk_widget().grid(row=0, column=2)
        ax3.legend(['Stock_Index_Price'])
        ax3.set_xlabel('Interest Rate')
        ax3.set_title('Interest Rate Vs. Stock Index')

    def content(self):
        ''''
        Create users page components
        '''

        tools_frame = ttk.Frame(
            self
        )

        self.charts_frame = ttk.Frame(
            self
        )

        users_card = ttk.Frame(
            tools_frame
        )

        ttk.Label(
            users_card,
            text='Statistics',
            image=self.assets['settings'],
            compound='top',
            font='Helvetica 15',
            foreground='#4f4f4f',
            borderwidth=2
        ).grid(column=0, row=0)

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

        tools_frame.grid(column=0, row=1, padx=10, pady=5, sticky='nw')

        self.draw_charts()

        self.charts_frame.grid(column=0, row=2, pady=5, padx=10, sticky='s')

    