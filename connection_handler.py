
from mysql import connector
from constants import HOST, PASSWORD, USER


class ConnectionHandler:
  
  def __init__(self):
    pass

  def create_connection(self, sql, params=None):

    db = connector.connect(
      host=HOST,
      user=USER,
      password=PASSWORD,
      database="Billing_System",
      auth_plugin='mysql_native_password'
    )

    cursor = db.cursor(buffered=True)

    try:
      cursor.execute(sql, params)
      db.commit()

      if params:
        return cursor.rowcount

      resp = [x for x in cursor.fetchall()]
      return resp

    except Exception as e:
      print(e)
      return self.to_object(status="Error", message="An error occured")


  def login_authenticate(self, creds, role):
    sql = "select * from Admin_Account" if role == "admin" else "select * from Cashier_Account"
    try:
      connect = self.create_connection(sql)
      for user in connect:
        if user[1].lower() == creds["username"].lower():
          if user[2] == creds["password"]:
            return self.to_object("Success", "Logged in successfully")

      return self.to_object("Error", "Incorrect Username or Password")

    except:
      return self.to_object("Error", "An Error Occurred")

  
  def save_new_product(self, product):
    insert_sql = "INSERT INTO In_Stocks(Items, Price, Item_image_link, Quantity) \
            VALUES (%s, %s, %s, %s)"
    
    try:
      insert_values = self.create_connection(insert_sql, product)
      return self.to_object(status="Success", message=insert_values)

    except:
      return self.to_object(status="Error", message="An error occured")
  

  def get_products(self):
    sql = "SELECT * FROM In_Stocks"

    try:
      resp = self.create_connection(sql)
      return self.to_object(status="Success", message=resp)

    except Exception as e:
      print(e)
      return self.to_object(status="Error", message="An error occured")


  def to_object(self, status, message):
    resp = {}
    resp["status"] = status
    resp["message"] = message

    return resp