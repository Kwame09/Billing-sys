from datetime import datetime
from typing import Dict, List, Type
import uuid


from common import Database
from common import Utils

class Model():
    '''A model class'''
    TABLE_NAME = ''
    SELECTED_COLUMNS = []
    WHERE_CLAUSE = []
    GROUP_BY = ''
    ORDER_BY = ()
    LIMIT = 0

    def __init__(self, created_at=None, updated_at=None, id=None):
        self.created_at = (datetime.utcnow()).strftime("%a %b %d %Y %H:%M:%S") \
            if not created_at else created_at
        self.updated_at = (datetime.utcnow()).strftime("%a %b %d %Y %H:%M:%S") \
            if not updated_at else updated_at
        self.id = uuid.uuid4() if not id else str(id)

    def save(self):
        '''
        Instance Method for saving Model instance to database

        @params None
        @return None
        '''

        data = {}

        return Database.insert(Model.TABLE_NAME, data)
    
    @classmethod
    def clear(cls):
        '''
        Clear all Class settings
        '''
        cls.SELECTED_COLUMNS = []
        cls.WHERE_CLAUSE = []
        cls.GROUP_BY = ''
        cls.ORDER_BY = ()
        cls.LIMIT = 0
    
    @classmethod
    def select(cls, columns: str):
        '''
        Class Method for retrieving model \n
        grouped by specified column

        @param column Column Name to group by
        @return Class
        '''

        cls.SELECTED_COLUMNS = columns
        return cls
    
    @classmethod
    def where(cls, clause: str):
        '''
        Class Method for retrieving model \n
        grouped by specified column

        @param column Column Name to group by
        @return Class
        '''

        cls.WHERE_CLAUSE.append(clause)
        return cls
    
    @classmethod
    def group_by(cls, column: str):
        '''
        Class Method for retrieving model \n
        grouped by specified column

        @param column Column Name to group by
        @return Class
        '''

        cls.GROUP_BY = column
        return cls
    
    @classmethod
    def order_by(cls, column: str, order: str = 'ASC'):
        '''
        Class Method for retrieving model \n
        ordered by specified column

        @param column Column Name to group by
        @return Class
        '''

        cls.ORDER_BY = (column, order.upper())
        return cls
    
    @classmethod
    def limit(cls, count: int = 0, offset: int = 0):
        '''
        Class Method for retrieving model \n
        ordered by specified column

        @param column Column Name to group by
        @return Class
        '''

        cls.LIMIT = f"{count}"
        if offset:
            cls.LIMIT += f", {offset}"
        return cls

    @classmethod
    def update(cls, id, update: Dict):
        '''
        Class Method for updating model in database

        @param update Content to be update in dictionary format
        @return None
        '''

        return Database.update(cls.TABLE_NAME, id, update)
    
    @classmethod
    def delete(cls, id):
        '''
        Class Method for updating model in database

        @param update Content to be update in dictionary format
        @return None
        '''

        return Database.delete(cls.TABLE_NAME, id)
    
    @classmethod
    def count(cls, params: dict = None)-> int:
        '''
        Class Method for counting Model Projects

        @params None
        @return int Count of Projects
        '''
        
        if params is not None:
            return Database.count(cls.TABLE_NAME, params)
            
        return Database.count(cls.TABLE_NAME)
    
    @classmethod
    def sum(cls, column: str)->int:
        '''
        Class method for retrieving sum of\n
        of specified column in table

        @params None
        @return int Sum of column
        '''
        return Database.sum(cls.TABLE_NAME, column)

    @classmethod
    def get(cls, _id = None):
        '''
        Class Method for retrieving model \n
        model data from database

        @param _id ID of Model
        @return List[Model] instance(s)
        '''

        if _id is not None:
            model = Database.find_one(cls.TABLE_NAME, {'id': _id})
            return cls(**model) if model else None
        
        query = 'SELECT '
        if cls.SELECTED_COLUMNS:
            query += cls.SELECTED_COLUMNS if type(cls.SELECTED_COLUMNS) is str \
                else ', '.join(cls.SELECTED_COLUMNS)
        else:
            query += "*"
        
        query += f" FROM {cls.TABLE_NAME}"

        if len(cls.WHERE_CLAUSE):
            query += " WHERE"
            for clause in cls.WHERE_CLAUSE:
                if type(clause) is str:
                    query += f" ({clause}) AND"
                elif type(clause) is dict:
                    query += ' ('
                    for key, value in clause.items():
                        query += f"{key}='{value}' AND "
                    query = query.rstrip('AND ').strip()
                    query += ') AND'
        
        query = query.rstrip('AND').strip()
        if cls.GROUP_BY:
            query += f" GROUP BY {cls.GROUP_BY}"
        
        if len(cls.ORDER_BY):
            query += f" ORDER BY {cls.ORDER_BY[0]} {cls.ORDER_BY[1]}"
        
        if cls.LIMIT:
            query += f" LIMIT {cls.LIMIT}"
        
        cls.clear()
        
        return Database.query(query)
    
    @classmethod
    def all(cls)->list:
        '''
        Class Method for retrieving all \n
        model data from database

        @param _id ID of the function in database
        @return List[Model] instance(s)
        '''

        return [cls(**elem) for elem in Database.find(cls.TABLE_NAME)]
    
    @classmethod
    def find(cls, params: dict)-> list:
        '''
        Class Method for retrieving models
        by provided parameters

        @param params
        @return List[Model]
        '''

        return [cls(**elem) for elem in Database.find(cls.TABLE_NAME, params)]
    
    @classmethod
    def search(cls, columnname: str, search: str)->list:
        '''
        Class Method for retrieving model data
        specified column values

        @param name
        @return List[Model] Model instances
        '''

        sql = f"SELECT * from {cls.TABLE_NAME} WHERE "
        sql += f"{columnname} LIKE '%{search}%'"
        
        return [cls(**elem) for elem in Database.query(sql)]
    
    @classmethod
    def query(cls, where_clause: str)->list:
        '''
        Class Method for retrieving model data
        by where clause

        @param name
        @return List[Model] Model instances
        '''

        sql = f"SELECT * from {cls.TABLE_NAME} WHERE "
        sql += f"{where_clause}"
        
        return [cls(**elem) for elem in Database.query(sql)]
    
    def json(self)-> Dict:
        '''
        Instance Method for converting Model Instance to Dict

        @paramas None
        @return dict() format of Function instance
        '''

        return {}
