#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os.path
import json

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
            
            if all(x is not None for x in (name, OS_type, IP, path)):
                
                # Get location space
                # ...
                
                # Insert location
                self.data.DB.insert('Locations', name=name, OS_type=OS_type, IP=IP, path=path)
        
        # ---------------------------------------
        #   MODIFY
        # ---------------------------------------
        
        if self.inputs.getvalue('action_modify') is not None:
            
            id = self.inputs.getvalue('id')
            name = self.inputs.getvalue('name')
            OS_type = self.inputs.getvalue('OS_type')
            IP = self.inputs.getvalue('IP')
            path = self.inputs.getvalue('path')
            
            if all(x is not None for x in (id, name, OS_type, IP, path)):
                
                # Update location
                self.data.DB.update('Locations', 'name', name, 'id=?', id)
                self.data.DB.update('Locations', 'IP', IP, 'id=?', id)
                self.data.DB.update('Locations', 'OS_type', OS_type, 'id=?', id)
                self.data.DB.update('Locations', 'path', path, 'id=?', id)
                
        # ---------------------------------------
        #   DELETE
        # ---------------------------------------
        
        if self.inputs.getvalue('action_delete') is not None:
            
            id = self.inputs.getvalue('id')
            
            if id is not None:
                
                # Delete location
                self.data.DB.delete('Locations', 'id=?', id)
        
        # ---------------------------------------
        #   UPDATE
        # ---------------------------------------
        
        if self.inputs.getvalue('action_update') is not None:
            
            pass
        
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
        
        H.jsfile('Core/JS/locations.js')
        
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
            
        H.p(cont);
        H.a(0, '?spot=locations&id=new')
        H.text(0, ('New storage location', 'Nouvel espace de stockage'))
             
        if lid is not None:
       
            # ---------------------------------------
            #   LOCATION
            # ---------------------------------------
          
            if lid=='new':
                
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
                
            else:
       
                # --- Get user infos
                loc = self.data.DB.single('SELECT * FROM Locations WHERE id=?', lid)
                
                if loc is not None:
                
                    # ---------------------------
                    #   LOCATION SETTINGS
                    # ---------------------------
                    
                    cont = H.div(main, cls='cont')
                    
                    H.h2(cont)
                    H.text(0, ('Storage location settings',"Paramètres de l'espace de stockage"))
                    
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
                    H._select(0, opt={'linux': "Linux", 'windows': "Windows"}, select=loc['OS_type'], name='OS_type')
                    
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
                    H._submit(0, ('Save', 'Enregistrer'), name='action_modify')
        
                    # ---------------------------
                    #   LOCATION STORAGE
                    # ---------------------------
                    
                    jpath = '{0}Trees/{1}.json'.format(self.settings.get('root'), loc['name'])
                    
                    cont = H.div(main, cls='cont')
                    
                    H.h2(cont)
                    H.text(0, ('Storage scheme','Schéma de stockage'))

                    H.p(cont)
                    H.text(0, 'File path:')
                    H.span(0, id='jpath')
                    H.text(0, jpath)

                    # === UPDATE STORAGE SCHEME ============================

                    H._submit(cont, ('Update scheme', 'Actualiser'), id='update')
                    H._submit(cont, ('Stop', 'Stop'), id='stop_update')
                    
                    # --- Update table
                    
                    H.table(cont, id='cont_update')
                    
                    H.tr()
                    H.td(rowspan='2', width='200px')
                    H.img(0, 'Core/Style/updating.gif', width='100px');
                    
                    H.td(width='99%')
                    H.text(0, 'Current folder: ')
                    H.span(0, id='current_folder')
                    H.text(0, '')
                    
                    H.tr()
                    ucont = H.td()
                    H.div(ucont, id='cont_update_folders')
                    H.span(0, cls='update_num', id='update_folders')
                    H.text(0, '0')
                    H.span(-1)
                    H.text(0, 'folders')
                    
                    H.div(ucont, id='cont_update_files')
                    H.span(0, cls='update_num', id='update_files')
                    H.text(0, '0')
                    H.span(-1)
                    H.text(0, 'files')

                    H.div(ucont, id='cont_update_size')
                    H.span(0, cls='update_num', id='update_size')
                    H.text(0, '0 B')

                    # === DISPLAY STORAGE SCHEME ===========================
                    
                    if os.path.exists(jpath):
                        
                        tree = self.get_json(jpath)
                        H.pre(cont)
                        H.text(0, tree);
                        
                        
    # ----------------------------------------------------------------------
    def get_json(self, jpath):
        '''
        Build display.
        
        Inputs:
            - L     (list)  The list
            
        Outputs:
            - out   (str)   The string for display
        '''
        
        # --- Get List from json file
        f = open(jpath, 'r')
        L = json.load(f)
        f.close()
        
        out = ''
        for i, x in enumerate(L):
            
            # --- Find level
            
            pre = ''
            parent = x[0]
            while parent is not None:
                if parent in [item[0] for item in L[i+1:]]:
                    if parent is x[0]:
                        # pre += '─├ '
                        pre += '-- '
                    else:
                        # pre += ' │ '
                        pre += ' | '
                else:
                    if parent is x[0]:
                        # pre += '─└ '
                        pre += '-- '
                    else:
                        pre += '   '
                parent = L[parent][0]
            out += pre[::-1]
            
            # --- Size on disk
            tmp = '[' + self.hsize(x[2]) + ']'
            out += tmp + ' '*(10-len(tmp))
            
            # --- Name
            if x[1]==-1:     # Link
                out += '    <span style="color:#6F0; font-weight: bold;">' + x[3] + '</span> -> ' + x[4]
            
            elif x[1]==0:     # Directory
                out += '    <b>' + x[3] + '</b>'
                    
            elif x[1]==1:   # File
                out += '    <span style="color:#36C;">' + x[3] + '</span>'
            else:           #Group
                out += '    <span style="color:#399;">' + x[3] + '</span> [' + str(x[1]) + ' files]'
                    
            out += '\n'
                
        return out
    
   
    # --------------------------------------------------------------------------
    def hsize(self, num, suffix='B'):
    
        for unit in ['','k','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Y', suffix)
    