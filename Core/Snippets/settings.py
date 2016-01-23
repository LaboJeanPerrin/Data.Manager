#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from Snippets.database import DB

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ==========================================================================
class Settings:
    '''
    The Settings class
    '''
    
    LANGUAGES = ['en','fr']
    IMAGE = ['png', 'jpg', 'jpeg', 'svg', 'bmp', 'gif', 'tif', 'tiff', 'eps']
    VIDEO = ['avi', 'mp4', 'mpeg', 'ogv', '.h264']
    
    # ----------------------------------------------------------------------
    def __init__(self):
        '''
        Constructor
        
        Inputs:
            -
        '''
        
        self.settings = {'root':os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/'}
        self.DB = DB('Settings.db')
        
    # ----------------------------------------------------------------------
    def get(self, key):
        '''
        Get accessor
        
        Inputs:
            key (str) The key to accessor
            
        Output:
            The value setting
        '''

        return self.settings[key]

    # ----------------------------------------------------------------------
    def set(self, key, value):
        '''
        Set accessor
        
        Inputs:
            key (str)       The key to accessor
            vaalue (str)    The value to update
            
        Output:
            None
        '''

        self.settings[key] = value

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --------------------------------------------------------------------------
def get_settings():

    S = Settings()
    
    for row in S.DB.multi('SELECT * FROM General'):
        S.settings[row[0]] = row[1]

    return S