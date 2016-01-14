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
            
            name = self.inputs.getvalue('name')
            OS_type = self.inputs.getvalue('OS_type')
            IP = self.inputs.getvalue('IP')
            path = self.inputs.getvalue('path')
            
            print(name, OS_type, IP, path)
            
            if name is not None and OS_type is not None and IP is not None and path is not None:
                
                # Get location space
                print(self.inputs)
                
                # Insert location
                self.data.DB.insert('Locations', name=name, OS_type=OS_type, IP=IP, path=path)
        
        
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
        lid = self.inputs.getvalue('id')
        
        # --- Definitions
        H = self.html
        
        # --- Head
        H.style('locations')
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
        H.text(0, ('Storage locations', 'Espaces de stockage'))
        
        H.br(cont)
        
        ll = H.span(cont, id='loc_list')
        for loc in self.data.DB.multi('SELECT * FROM Locations'):
            
            if str(loc['id'])==str(lid):
                H.a(ll, '?spot=locations&id={0}'.format(loc['id']), id='loc_selected')
            else:
                H.a(ll, '?spot=locations&id={0}'.format(loc['id']))
            H.text(0, loc['name'])
                
        # ---------------------------------------
        #   LOCATION
        # ---------------------------------------
                
        if lid is not None:
            
            # --- Get user infos
            loc = self.data.DB.single('SELECT * FROM Locations WHERE id=?', lid)
            
            if loc is not None:
            
                cont = H.div(main, cls='cont')
                
                H.h2(cont)
                H.text(0, ('Storage location info','Information espace de stockage'))
                
                H.form(cont)
                H.table(0, cls='loc_table')

                # --- Delete
                H.tr()
                H.td(colspan='2')
                H.center(0)
                H._submit(0, ('Delete storage location', 'Supprimer cet espace de stockage'), name='action_delete', 
                        onclick="return confirm('{0} {1}?');".format(self.mlt(('Do you really want to delete', 'Voulez-vous vraiment supprimer')), loc['name']))

                # --- Location id
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Location id', 'Identifiant'))
                
                H.td()
                H.span(0, cls='form_txt')
                H.text(0, '{0}'.format(loc['id']))

                # --- Name
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Name', 'Nom'))
                
                H.td()
                H._text(0, name='name', value=loc['name'])
                
                # --- IP
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('IP address', 'Adresse IP'))
                
                H.td()
                H._text(0, name='IP', value=loc['IP'])

                # --- OS type
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Operating system', "Système d'exploitation"))
                
                H.td()
                H._select(0, opt={'linux': "Linux", 'windows': "Windows"}, name='OS_type')
                
                # --- Path
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Data path', 'Répertoire de données'))
                
                H.td()
                H._text(0, name='path', value=loc['path'])
                
                # --- Space
                H.tr()
                H.td(cls='form_item')
                H.p(0)
                H.text(0, ('Storage space', 'Volume de stockage'))
                
                H.td()
                H.span(0, cls='form_txt')
                if loc['space'] is not None:
                    H.text(0, loc['space'])
                else:
                    H.text(0, ("Undefined", "Indéfini"))
                    
                # --- Validate
                H.tr()
                H.td(colspan='2')
                H.center(0)
                H._submit(0, ('Save', 'Enregistrer'), name='action_save')
                
        # ---------------------------------------
        #   NEW LOCATION
        # ---------------------------------------
        
        cont = H.div(main, cls='cont')
        
        H.h2(cont)
        H.text(0, ('Add storage location','Nouvel espace de stockage'))
        
        H.form(cont)
        H.table(0, cls='loc_table')

        # --- Name
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Name', 'Nom'))
        
        H.td()
        H._text(0, name='name')
        
        # --- IP
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('IP address', 'Adresse IP'))
        
        H.td()
        H._text(0, name='IP', value='134.157.132.')

        # --- OS type
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Operating system', "Système d'exploitation"))
        
        H.td()
        H._select(0, opt={'linux': "Linux", 'windows': "Windows"}, name='OS_type')
        
        # --- Path
        H.tr()
        H.td(cls='form_item')
        H.p(0)
        H.text(0, ('Data path', 'Répertoire de données'))
        
        H.td()
        H._text(0, name='path')
        
        # --- Validate
        H.tr()
        H.td(colspan='2')
        H.center(0)
        H._submit(0, ('Create storage location', 'Ajouter cet espace de stockage'), name='action_create')