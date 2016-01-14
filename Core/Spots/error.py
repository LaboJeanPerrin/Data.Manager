#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Spot import Spot

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
        
        # --- Style
        H.style('error')
        
        # Main containers
        H.div(0, id='container')
        
        # Language chooser
        self.language_chooser()
        
        H.br(0)
        
        # Title
        H.h1(0)
        H.text(0, ("Error !", "Erreur !"))

        # Image
        H.img(-1, 'Core/Style/Icons/Robots/Broken.png', id='image', width='256px')
        
        # Text
        H.p(-1)
        H.text(0, ("Your request could not be completed.", "Votre requête n'a pas pu aboutir."))
        
        H.p(-1)
        H.a(0, "?spot=home")
        H.text(0, ("Back to home", "Retour à l'accueil"))

    