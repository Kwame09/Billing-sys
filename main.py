
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from connection_handler import ConnectionHandler
from PIL import ImageTk, Image
import os


supermarket_app = Tk()
supermarket_app.title("Supermarket Billing System")
supermarket_app.geometry("1920x1080")

class AdminPage:
  #img_url = "./assets/add_img.png"
  const_url = "add_img.png"
  img_url = os.path.realpath(os.path.join(os.curdir, 'assets', const_url))
  add_img = ImageTk.PhotoImage(Image.open(img_url).resize((300, 100)))

  def __init__(self, app):
    self.app = app

  def set_image_url(self, url):
    self.img_url = url
    add_img_label.place_forget()
    self.add_img = ImageTk.PhotoImage(Image.open(url).resize((200, 100)))
    add_img_btn["image"] = self.add_img
    add_img_btn.place_configure(anchor="c", relx=0.5, rely=0.25)
    img_display_label.place(anchor="c", relx=0.5, rely=0.33)

  def get_file(self):
    filename = filedialog.askopenfilename()
    self.set_image_url(filename)

  def return_image(self, url):
    return ImageTk.PhotoImage(Image.open(url).resize((300, 100)))

  def add_products(self):
    global add_img_btn, add_img_label, img_display_label
    add_products_page = Frame(
      self.app,     
      width="1920", 
      height="1080",
    )
    top_label = Label(
      add_products_page, 
      text="ADD PRODUCT DETAILS", 
      fg="blue",
      font="Times 20 bold"
    )
    top_label.place(anchor="c", relx=0.5, rely=0.15)
    add_img_label = Label (
      add_products_page,
      image=self.add_img
    )
    add_img_label.place(anchor="c", relx=0.5, rely=0.25)
    add_img_btn = Button(
      add_products_page,
      text="Select Image",
      command=self.get_file
    )
    add_img_btn.place(anchor="c", relx=0.5, rely=0.35)
    img_display_label = Label(
      add_products_page,
      text="Click on image to change"
    )

    product_name_label = Label(
      add_products_page,
      text="Product name"
    )
    product_name_label.place(anchor="c", relx=0.5, rely=0.4)
    product_name_var = StringVar()
    product_name_entry = Entry(
      add_products_page,
      textvariable=product_name_var
    )
    product_name_entry.place(anchor="c", relx=0.5, rely=0.45)

    product_quantity_label = Label(
      add_products_page,
      text="Product quantity"
    )
    product_quantity_label.place(anchor="c", relx=0.5, rely=0.5)
    product_quantity_var = IntVar()
    product_quantity_entry = Entry(
      add_products_page,
      textvariable=product_quantity_var
    )
    product_quantity_entry.place(anchor="c", relx=0.5, rely=0.55)

    product_price_label = Label(
      add_products_page,
      text="Product price"
    )
    product_price_label.place(anchor="c", relx=0.5, rely=0.6)
    product_price_var = DoubleVar()
    product_price_entry = Entry(
      add_products_page,
      textvariable=product_price_var
    )
    product_price_entry.place(anchor="c", relx=0.5, rely=0.65)

    def save_product():
      product = (
        product_name_var.get(), 
        product_price_var.get(),
        self.img_url,
        product_quantity_var.get()
      )
      
      connection = ConnectionHandler()
      resp = connection.save_new_product(product)
      if resp["status"] == "Success":
        messagebox.showinfo("Status", "Product added successfully")
        yes_no = messagebox.askyesnocancel(
          "Add product", 
          "Do you want to add another item?"
        )

        if (yes_no):
          product_name_var.set("")
          product_price_var.set(0.0)
          product_quantity_var.set(0)
          self.add_img = ImageTk.PhotoImage(Image.open(self.const_url).resize((200, 100)))
          add_img_btn["image"] = self.add_img

      else:
        messagebox.showerror("Error", "An Error Occurred")

    save_product = Button(
      add_products_page,
      text="Save Product",
      command=save_product
    )
    save_product.place(anchor="c", relx=0.5, rely=0.7)
    add_products_page.place(anchor="c", relx=0.5, rely=0.5)

  def get_products(self):
    conn = ConnectionHandler()
    resp = conn.get_products()

    item_list = []
    
    get_products_page = Frame(
      self.app,
      width="1920", 
      height="1080"
    )

    if resp["status"] == "Success":
      pointer = 0
      mv_x = 0.1
      mv_y = 0.2
      for x in resp["message"]:
        if pointer != 0 and pointer % 6 == 0:
          mv_y += 0.3
          mv_x = 0.1

        item_frame = Frame(get_products_page, width=250, height=250)
        image = Label(
          item_frame,
          text="New",
          image=self.return_image(x[3]),
          width=150,
          height=150,
          bg="red"
        )
        image.place(anchor="c", relx=0.5, rely=0.5)
        item_frame.place(anchor="c", relx=mv_x, rely=mv_y)
        item_list.append(item_list)
        pointer += 1
        mv_x += 0.15

    get_products_page.place(anchor="c", relx=0.5, rely=0.5)

  def homepage(self):
    admin_page_handler = Frame(
      self.app, 
      width="1920", 
      height="1080"
    )

    btns_frame = Frame(
      admin_page_handler, 
      width=800, 
      height=600, 
    )

    top_label = Label(
      btns_frame, 
      text="SELECT AN ACTION", 
      fg="blue",
      font="Times 20 bold"
    )
    top_label.place(anchor="c", relx=0.5, rely=0.1)
    add_products_btn = Button(
      btns_frame,
      text="ADD PRODUCTS",
      width=18,
      height=4,
      font="Times 12",
      command=lambda: (admin_page_handler.place_forget(), self.add_products())
    )
    add_products_btn.place(anchor="c", relx=0.38, rely=0.3)
    get_products_btn = Button(
      btns_frame,
      text="GET PRODUCTS",
      width=18,
      height=4,
      font="Times 12",
      command=lambda: (admin_page_handler.place_forget(), self.get_products())
    )
    get_products_btn.place(anchor="c", relx=0.62, rely=0.3)
    add_users_btn = Button(
      btns_frame,
      text="ADD USERS",
      width=18,
      height=4,
      font="Times 12"
    )
    add_users_btn.place(anchor="c", relx=0.38, rely=0.5)
    check_sales_btn = Button(
      btns_frame,
      text="CHECK SALES",
      width=18,
      height=4,
      font="Times 12"
    )
    check_sales_btn.place(anchor="c", relx=0.62, rely=0.5)

    btns_frame.place(anchor="c", relx=0.5, rely=0.5)
    admin_page_handler.place(anchor="c", relx=0.5, rely=0.5)
  



def login(role):
  global handler
  handler.place_forget()
  login_handler = Frame(
    supermarket_app, 
    width="1920", 
    height="1080"
  )

  Label(
    login_handler, 
    text="Enter credentials to proceed"
  ).place(anchor="c", relx=0.5, rely=0.2)

  Label(
    login_handler, 
    text="Enter Username"
  ).place(anchor="c", relx=0.5, rely=0.3)

  username_var = StringVar()
  username_entry = Entry(
    login_handler, 
    textvariable=username_var, 
    width=20
  )
  username_entry.place(anchor="c", relx=0.5, rely=0.35)

  password_var = StringVar()
  Label(
    login_handler, 
    text="Enter Password"
  ).place(anchor="c", relx=0.5, rely=0.4)
  password_entry = Entry(
    login_handler, 
    textvariable=password_var, 
    width=20
  )
  password_entry.place(anchor="c", relx=0.5, rely=0.45)

  def authenticate():
    username = username_var.get()
    password = password_var.get()
    creds = {"username": username, "password": password}
    connection = ConnectionHandler()
    resp = connection.login_authenticate(creds, role)
    messagebox.showerror("Login status", resp.get("message"))
    if resp.get("status") == "Success":
      login_handler.place_forget()
      admin_window = AdminPage(supermarket_app)
      admin_window.homepage()

  Button(
    login_handler, 
    text="LOGIN",
    command=authenticate
  ).place(anchor="c", relx=0.5, rely=0.5)

  login_handler.place(anchor="c", relx=0.5, rely=0.5)

def cashier_login():
  pass


handler = Frame(
  supermarket_app, 
  width="1920", 
  height="1080"
)

# homepage_title = Label(
#   handler, 
#   text="SUPERMARKET BILLING SYSTEM", 
#   fg="blue",
#   font="Times 20 bold"
# )

# cashier_login_btn = Button(
#   handler, 
#   text="Cashier Login", 
#   width=30, 
#   height=5, 
#   command=lambda: login("cashier"),
#   font="Times 15 bold"
# )

# admin_login_btn = Button(
#   handler, 
#   text="Admin Login", 
#   width=30, 
#   height=5,
#   command=lambda: login("admin"),
#   font="Times 15 bold"
# )

# homepage_title.place(anchor="c", relx=0.5, rely=0.2)
# cashier_login_btn.place(anchor="c", relx=0.5, rely=0.35)
# admin_login_btn.place(anchor="c", relx=0.5, rely=0.5)
handler.place(anchor="c", relx=0.5, rely=0.5)

new_page = AdminPage(supermarket_app)
new_page.homepage()

supermarket_app.mainloop()

  # home_btn = Button(
    #   admin_page_handler, 
    #   text="Home", 
    #   width="20"
    # )
    # home_btn.place(anchor="c", relx="0.045", rely="0.043")
    # pages_btn = Button(
    #   admin_page_handler, 
    #   text="Pages", 
    #   width="20",
    #   command=lambda: (
    #     admin_page_handler.place_forget(), 
    #     self.pages()
    #   )
    # )
    # pages_btn.place(anchor="c", relx="0.13", rely="0.043")
    # quit_btn = Button(
    #   admin_page_handler, 
    #   text="Help", 
    #   width="20"
    # )
    # quit_btn.place(anchor="c", relx="0.215", rely="0.043")