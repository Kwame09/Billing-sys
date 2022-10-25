from requests import session
from common.database import Database
from common.sessionmanager import SessionManager
from common.utils import Utils
from common.security import authenticate

identity = None

Database.initialize()
session = SessionManager()
session['user'] = None
current_user = session['user']