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
    def pre_process(self):
        '''
        Pre-processing method
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        Spot.pre_process(self)
        
        # ---------------------------------------
        #   CREATE
        # ---------------------------------------
        
        if self.inputs.getvalue('action_create') is not None:
            
            email = self.inputs.getvalue('email')
            password = self.inputs.getvalue('password')
            firstname = self.inputs.getvalue('firstname')
            lastname = self.inputs.getvalue('lastname')
            
            if firstname is not None and lastname is not None and email is not None and password is not None:
                
                self.data.DB.insert('Users', email=email, password=password, firstname=firstname, lastname=lastname)
        
        # ---------------------------------------
        #   DELETE
        # ---------------------------------------
        
        if self.inputs.getvalue('action_delete') is not None:
            
             self.data.DB.delete('Users', 'id=?', self.inputs.getvalue('id'))
        
        # ---------------------------------------
        #   UPDATE
        # ---------------------------------------
        
        if self.inputs.getvalue('action_save') is not None:
            
            # User id
            uid = self.inputs.getvalue('id')
            
            # Firstname
            self.data.DB.update('Users', 'firstname', self.inputs.getvalue('firstname'), 'id=?', uid)
            
            # Lastname
            self.data.DB.update('Users', 'lastname', self.inputs.getvalue('lastname'), 'id=?', uid)
            
            # Email
            self.data.DB.update('Users', 'email', self.inputs.getvalue('email'), 'id=?', uid)
            
            # Password
            self.data.DB.update('Users', 'password', self.inputs.getvalue('password'), 'id=?', uid)
        
    # ----------------------------------------------------------------------
    def set_html(self):
        '''
        Sets html code
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        # --- Parameters
        uid = self.inputs.getvalue('id')
        
        # --- Definitions
        H = self.html
        
        # --- Head
        H.style('users')
        H.style('menu')
        
        # --- Structure
        H.table(0, id='structure')
        H.tr()
        menu = H.td(id='menu_bar')
        main = H.td()
        
        # --- Main menu
        self.main_menu(menu)
        
        # ---------------------------------------
        #   MAIN
        # ---------------------------------------
        
        cont = H.div(main, cls='cont')
        
        H.h1(cont)
        H.text(0, ("Manage users", "Gestion des utilisateurs"))
        
        H.br(cont)
        
        ul = H.span(cont, id='user_list')
        for user in self.data.DB.multi('SELECT * FROM Users'):
            
            if str(user['id'])==str(uid):
                H.a(ul, '?spot=users&id={0}'.format(user['id']), id='user_selected')
            else:
                H.a(ul, '?spot=users&id={0}'.format(user['id']))
            H.text(0, '{0} {1}'.format(user['firstname'], user['lastname']))
                
        # ---------------------------------------
        #   USER
        # ---------------------------------------
                
        if uid is not None:
            
            # --- Get user infos
            user = self.data.DB.single('SELECT * FROM Users WHERE id=?', uid)
            
            if user is not None:
            
                cont = H.div(main, cls='cont')
                
                H.h2(cont)
                H.text(0, ('User info','Informations utilisateur'))
                
                H.form(cont)
                H.table(0, cls='user_table')

                # --- Delete
                H.tr()
                H.td(colspan='2')
                H.center(0)
                H._submit(0, ('Delete user', 'Supprimer cet utilisateur'), name='action_delete', 
                        onclick="return confirm('{0} {1} {2}?');".format(self.mlt(('Do you really want to delete', 'Voulez-vous vraiment supprimer')), user['firstname'], user['lastname']))

                # --- User id
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('User id', 'Identifiant'))
                
                H.td()
                H.text(0, '<b><pre>{0}</pre><b>'.format(user['id']), decode=False)
                
                # --- Firstname
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Firstname', 'Prénom'))
                
                H.td()
                H._text(0, name='firstname', value=user['firstname'])

                # --- Lastname
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Lastname', 'Nom de famille'))
                
                H.td()
                H._text(0, name='lastname', value=user['lastname'])
                
                # --- Email
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Email', 'Courriel'))
                
                H.td()
                H._text(0, name='email', value=user['email'])
                
                # --- Password
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Password', 'Mot de passe'))
                
                H.td()
                H._text(0, name='password', value=user['password'])
                
                # --- Validate
                H.tr()
                H.td(colspan='2')
                H.center(0)
                H._submit(0, ('Save', 'Enregistrer'), name='action_save')
            
        # ---------------------------------------
        #   NEW USER
        # ---------------------------------------
        
        cont = H.div(main, cls='cont')
        
        H.h2(cont)
        H.text(0, ('Add user','Nouvel utilisateur'))
        
        H.form(cont)
        H.table(0, cls='user_table')
        
        # --- Firstname
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Firstname', 'Prénom'))
        
        H.td()
        H._text(0, name='firstname')

        # --- Lastname
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Lastname', 'Nom de famille'))
        
        H.td()
        H._text(0, name='lastname')
        
        # --- Email
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Email', 'Courriel'))
        
        H.td()
        H._text(0, name='email')
        
        # --- Password
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Password', 'Mot de passe'))
        
        H.td()
        H._text(0, name='password')
        
        # --- Validate
        H.tr()
        H.td(colspan='2')
        H.center(0)
        H._submit(0, ('Create user', 'Ajouter cet utilisateur'), name='action_create')
    