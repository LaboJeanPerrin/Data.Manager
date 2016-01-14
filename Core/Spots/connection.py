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
    def pre_process(self):
        '''
        Pre-processing method
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        Spot.pre_process(self)
        
        # --- Check for disconnection
        
        # Check user in the database
        res = self.session.DB.single('SELECT * FROM Sessions WHERE sid=?', self.session.id)
        
        if res['user'] is not None:
            
            # Remove the user from the database
            self.session.DB.update('Sessions', 'user', None, 'sid=?', self.session.id)
            
            # Update the session
            self.session.user = None
        
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
        H.style('connection')
        
        # Main containers
        H.div(0, id='container')
                
        # Language chooser
        self.language_chooser()
        
        H.br(0, 1)
        
        # Title
        H.h1(0)
        H.text(0, ("Welcome to Data Manager", "Bienvenue sur <i>Data Manager</i>"), decode=False)

        # Form
        H.form(-1, action='?')
        H._hidden(0, 'form_action', 'connect')

        H.table(0, id='tab')
        
        # ---
        H.tr()
        H.td()
        H.p(0)
        H.text(0, ("Email", "E-mail"))
        
        H.td()
        H._text(0, name='email')
        
        # ---
        H.tr()
        H.td() 
        H.p(0)
        H.text(0, ("Password", "Mot de passe"))
        
        H.td()
        H._password(0, name='password')
    
        # ---
        H.tr()
        H.td(colspan='2')
        H._submit(0, ("Submit", "Valider"))
    
    # ----------------------------------------------------------------------
    def form_action(self):
        '''
        Form actions
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        # --- Check login/password
        res = self.data.DB.single("SELECT * FROM Users WHERE `email`=?", self.inputs.getvalue('email'))
       
        if res['password']==self.inputs.getvalue('password'):
        
            # Update user in the database
            self.session.DB.update('Sessions', 'user', res['id'], 'sid=?', self.session.id)
        
            # Redirection
            self.redirect('?spot=home')
            return True
        
        else:
            
            print('--- Conection not allowed ---')
        
        