from models.user import User
from common import Utils


identity = None

def authenticate(username: str, password: str, role: str):
    '''
    Function for authenticating user

    @param email Email Address
    @param password Password
    @return User Instance or None
    '''
    global identity

    user = User.authenticate(username, role)
    if user:
        if Utils.check_hashed_password(password, user.password):
            identity = user
            return user
    return None


'''
def identity(payload):
    user_id = payload['identity']
    return User.get(user_id)
'''
