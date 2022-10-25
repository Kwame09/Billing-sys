from tkinter import *
from tkinter import ttk

from pages import LoginPage
from pages import MainLayoutPage

APP_NAME = "Supermarket Billing System"
APP_VERSION = '0.0.1'

supermarket_app = Tk()
supermarket_app.title(APP_NAME)

w = 400
h = 200

sw = supermarket_app.winfo_screenwidth()
sh = supermarket_app.winfo_screenheight()

x = (sw/3)
y = (sh/3)

supermarket_app.geometry("%dx%d+%d+%d"%(w,h,x,y))
supermarket_app.overrideredirect(False)

login_page = LoginPage(supermarket_app, x, y)
#mainlayout = MainLayoutPage(supermarket_app, x, y)

intro_frame = Frame(
    supermarket_app,
    width=400,
    height=200
)

def startup():
    global intro_frame

    #intro_frame.place_forget()
    login_page.initialize()

# loader = ttk.Progressbar(
#     intro_frame,
#     mode='determinate',
#     length=200,
#     maximum=100
# )

#loader.grid(column=0, row=0)

#intro_frame.after(50, loader.start)

#intro_frame.place(anchor='c', relx=0.5, rely=0.5)
# supermarket_app.after(50, startup)

# def exit():
#     supermarket_app.eval('::ttk::CancelRepeat')
#     supermarket_app.destroy()

# supermarket_app.wm_protocol('WM_DELETE_WINDOW', exit)
# supermarket_app.wait_window(supermarket_app)

startup()

supermarket_app.mainloop()


