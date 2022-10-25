from common import Database
from common import Utils
from models.model import Model


from common import Database


class User(Model):
    '''A model class for user'''
    TABLE_NAME = 'Users'

    def __init__(self, username, name, role, password, created_at=None, updated_at=None, id=None):
        super().__init__(created_at, updated_at, id)
        self.username = username
        self.name = name
        self.password = password
        self.role = role

    def add(self):
        '''
        Instance Method for saving Product instance to database

        @params None
        @return None
        '''

        data = {
            "name": self.name,
            "username": self.username,
            "role": self.role,
            "password": Utils.hash_password(self.password)
        }

        return Database.insert(User.TABLE_NAME, data)
    
    def is_admin(self):
        return self.role == 'admin'
    
    @classmethod
    def get_by_username(cls, username: str):
        '''
        Retrieve User from database by their username

        @param username
        @return User
        '''

        sql = f"SELECT * FROM Users WHERE username='{username}'"
        result = Database.query(sql)
        
        if result:
            return cls(**result[0])
        return False
    
    @classmethod
    def authenticate(cls, username: str, role: str):
        '''
        Retrieve User from database by their username

        @param username
        @return User
        '''

        sql = f"SELECT * FROM Users WHERE username='{username}' AND role='{role}'"
        result = Database.query(sql)
        
        if result:
            return cls(**result[0])
        return False
    
    
    def json(self)-> dict:
        '''
        Instance Method for converting Product Instance to Dict

        @paramas None
        @return dict() format of Function instance
        '''

        return {
            "id": str(self.id),
            "name": self.name,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }