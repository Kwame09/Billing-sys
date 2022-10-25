from common import Database
from models import Model
from models import Product

class SaleItem(Model):
    '''A model class for SaleItem'''
    TABLE_NAME = 'SaleItems'

    def __init__(self, sales_id, product_id, quantity, total, created_at=None, updated_at=None, id=None):
        super().__init__(created_at, updated_at, id)
        self.sales_id = sales_id
        self.product_id = product_id
        self.quantity = quantity
        self.total = total

    def save(self)->int:
        '''
        Instance Method for saving SaleItem instance to database

        @params None
        @return insert_id()
        '''

        data = {
            "sales_id": self.sales_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total": self.total
        }

        return Database.insert(SaleItem.TABLE_NAME, data)
    
    def product(self)-> Product:
        '''
        Retrieve SoldItem's Product details

        @params None
        @return Product
        '''

        return Product.get(self.product_id)

    @classmethod
    def get_by_sales(cls, sales_id: str):
        '''
        Retrieve SaleItems by their sales_id

        @param sales_id 
        @return List[SaleItem]
        '''
        params = {'sales_id': sales_id}

        return [cls(**elem) for elem in Database.find(SaleItem.TABLE_NAME, params)]
    
    def json(self)-> dict:
        '''
        Instance Method for converting SaleItem Instance to Dict

        @paramas None
        @return dict() format of Function instance
        '''

        return {
            "id": str(self.id),
            "sales_id": self.sales_id,
            "product": self.product().name,
            "quantity": self.quantity,
            "total": self.total,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
