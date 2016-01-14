#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Spot import Spot
from Snippets.database import DB

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class spot(Spot):
    
    # ----------------------------------------------------------------------
    def __init__(self, *args):
        '''
        The Spot constructor
        
        Inputs:
            *args Usually [settings, session, inputs]
        '''
        
        # --- Parent constructor
        Spot.__init__(self, *args)
        
        
    # ----------------------------------------------------------------------
    def set_html(self):
        '''
        Sets html code
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        # --- Definitions
        H = self.html
        
        # --- Head
        H.style('home')
        H.style('menu')
        
        # --- Structure
        H.table(0, id='structure')
        H.tr()
        menu = H.td(id='menu_bar')
        main = H.td(id='main')
        
        # --- Main menu
        self.main_menu(menu)
        
        # ---------------------------------------
        #   MAIN
        # ---------------------------------------
        
        cont = H.div(main, cls='cont')
        
        H.h1(cont)
        H.text(0, ('General settings', "Paramètres généraux"))
                