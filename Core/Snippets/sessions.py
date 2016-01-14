#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
import os, sys
import cgi                              # CGI
import uuid
from http.cookies import SimpleCookie
from datetime import datetime

from Snippets.database import DB

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ==========================================================================     
class Session():
    
    def __init__(self, cookie, settings, data):
        
        # Definitions
        self.cookie = cookie
        self.id = cookie['sid'].value
        self.DB = DB('Sessions.db')
                
        # --- Get session
        res = self.DB.single("SELECT * FROM Sessions WHERE sid=?", self.cookie['sid'].value)
        
        # No session ?
        if res is None:
           
            # Create session entry            
            self.DB.insert('Sessions',
                           sid = self.id,
                           user = None, 
                           lang = settings.get('default_language'), 
                           last_connection = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                           num_failed_conn = 0)
            # Get session
            res = self.DB.single("SELECT * FROM Sessions WHERE sid=?", self.id)
            
        # --- Get user info
        
        if res['user'] is None:
            self.user = None
            
        else:
            
            usr = data.DB.single('SELECT * FROM Users WHERE id=?', res['user'])
            if usr is None:
                self.user = None        # This should NOT happen
            else:    
                self.user = dict(usr)   # Convert to dictionnary
            
        self.language = res['lang']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
# ==========================================================================     
def get_session(inputs, settings, data):

    # --- Manage cookie
    cookie = SimpleCookie()
    string_cookie = os.environ.get('HTTP_COOKIE')

    # --- Check for reinitialization
    if inputs.getvalue('clear_session') is None and string_cookie:
        
        ''' Existing session '''
        
        cookie.load(string_cookie)
        sid = cookie['sid'].value
        
    else:
        
        ''' New session '''
        
        sid = uuid.uuid4()
        cookie['sid'] = sid

    return Session(cookie, settings, data)