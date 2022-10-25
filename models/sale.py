from common import Database
from models.model import Model
from models.saleitem import SaleItem

class Sale(Model):
    '''A model class for Sales'''
    TABLE_NAME = 'Sales'

    def __init__(self, total, user_id=1, created_at=None, updated_at=None, id=None):
        super().__init__(created_at, updated_at, id)
        self.total = total
        self.user_id = user_id

    def save(self)->int:
        '''
        Instance Method for saving Sales instance to database

        @params None
        @return insert_id()
        '''

        data = {
            "user_id": self.user_id,
            "total": self.total
        }

        return Database.insert(Sale.TABLE_NAME, data)
    
    def items_count(self)-> int:
        '''
        Instance Method for retrieving purchased Items

        @params None
        @return List[Saleitem]
        '''

        sql = f"SELECT SUM(quantity) as count FROM SaleItems WHERE sales_id={self.id}"

        saleitems = Database.query(sql)[0]
        
        return saleitems['count']
    
    def salesperson(self)-> dict:
        '''
        Instance Method for salesperson for current sale

        @params None
        @return dict Database result
        '''

        sql = f"SELECT * FROM Users WHERE id={self.user_id}"
        user = Database.query(sql)[0]
        if user:
            del user['password']
        return user
    
    def json(self)-> dict:
        '''
        Instance Method for converting Sales Instance to Dict

        @paramas None
        @return dict() format of Product instance
        '''

        return {
            "id": str(self.id),
            "total": self.total,
            "salesperson": self.salesperson(),
            "count": self.items_count(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
