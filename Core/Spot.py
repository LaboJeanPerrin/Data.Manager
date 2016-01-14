#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from time import time
import html.entities

from HTML import HTML

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ==========================================================================
class Spot:
    """
    The Spot class
    
    """
    
    # ----------------------------------------------------------------------
    def __init__(self, settings, session, data, inputs):

        # --- Definitions
        
        self.settings = settings
        self.session = session
        self.data = data
        self.inputs = inputs
        self.html = HTML(self)
        self.display = True;
        
        # --- Pre-processing
        self.pre_process()
        
        # --- Actions
        if self.inputs.getvalue('form_action') is not None:
            
            # NB: stop is for redirection
            stop = self.form_action()
            
        else:
            stop = None
            
        # --- Html
        if stop is None:    
            self.html.meta(Language=self.session.language)
            self.html.favicon('Core/Style/Icons/favicon.ico?v={0}'.format(time()))
            self.html.style('fonts')
            self.html.style('common')
            self.html.jsfile('Core/JS/jquery.js')
            self.html.jsfile('Core/JS/common.js')
            self.set_html()
        
    # ----------------------------------------------------------------------
    def pre_process(self):
        '''
        Pre-processing method
        
        Inputs:
            -
            
        Output:
            None
        '''
        
        # --- Set language
        self.set_lang()
        
    # ----------------------------------------------------------------------
    def set_html(self):
        '''
        Sets html code
        
        Inputs:
            -
            
        Output:
            None
        '''
        pass
    
    # ----------------------------------------------------------------------
    def set_lang(self):
        '''
        Determine spot language
        
        Inputs:
            -
            
        Output:
            None
        '''

        # self.session.language

        # --- Modification
        lang = self.inputs.getvalue('lang')
        if lang is not None and lang in self.settings.LANGUAGES:
            
            # Update database
            self.session.DB.update('Sessions', 'lang', lang, 'sid=?', self.session.id)
            
            # Update session
            self.session.language = lang

        # --- Conversion
        self.LangIdx = self.settings.LANGUAGES.index(self.session.language)
        
    # ----------------------------------------------------------------------
    def mlt(self, M, decode=True, newlines=True):
        '''
        Multi-language text handler
        
        Inputs:
            M (tuple)             The text in many languages
            decode (bool=true)    Decode html or not
            newlines (bool=true)  Convert newlines ('\n' -> '<br>')
        
        Output:
            The text in the current language
        '''
        
        # --- Manage input
        if isinstance(M, str):
            tmp = M
        else:
            tmp = M[self.LangIdx]
        
        # --- Convert special chararters (decode)
        if decode:
            res = ''
            K = list(html.entities.entitydefs.keys())
            V = list(html.entities.entitydefs.values())
            
            for char in tmp:
                
                if char in V:
                    res += '&{0};'.format(K[V.index(char)])
                else:
                    res += char
            
        else:
            res = tmp
        
        # --- Convert newlines
        if newlines:
            res = str.replace(res, '\n', '<br>')
        
        # --- Return
        return res
      
    # ----------------------------------------------------------------------
    def truncate(self, s, limit=100, suffix='...'):
        '''
        Smart truncate
        
        Inputs:
            M (tuple) The text in many languages
        
        Output:
            The text in the current language
        '''
        if len(s) <= limit:
            return s
        else:
            return ' '.join(s[:limit+1].split(' ')[0:-1]) + suffix
    
    # ----------------------------------------------------------------------
    def redirect(self, location):
        '''
        Redirection (javascript based)
        
        Inputs:
            location (str) The new spot location
            
        Output
            None
        '''

        self.html.javascript('document.location.href="{0}"'.format(location))
        
    # ----------------------------------------------------------------------
    def language_chooser(self):
        '''
        Language chooser
        
        Inputs:
            -
            
        Output
            None
        '''
        
        # --- Store reference
        ref = self.html.ref
            
        # Language container
        self.html.div(0, id='language')
        
        if self.session.language != 'en':
            self.html.a(0, "?spot={0}&lang=en".format(self.settings.get('spot')))
            self.html.img(0, 'Core/Style/Icons/Flags/English.png')
        
        if self.session.language != 'fr':
            self.html.a(0, "?spot={0}&lang=fr".format(self.settings.get('spot')))
            self.html.img(0, 'Core/Style/Icons/Flags/French.png')

        # --- Restore reference
        self.html.ref = ref
        
    # ----------------------------------------------------------------------
    def main_menu(self, mid):
        '''
        Append the main menu.
        
        Inputs:
            None
            
        Output:
            None
        '''
        
        # Logo
        self.html.a(mid, '?spot=home')
        self.html.img(0, 'Core/Style/Logo.svg', id='logo')
        
        # Language chooser
        self.html.ref = mid
        self.language_chooser()
        
        self.html.a(0, '?spot=connection', id='disconnection')
        
        # Menu containers
        self.html.div(mid, id='menu')
        
        self.html.a(0, '?spot=settings', id="menu_Param", cls='menu_item')
        self.html.text(0, ("General settings", "Paramètres généraux"))
        
        self.html.a(-1, '?spot=users', id='menu_Users', cls='menu_item')
        self.html.text(0, ("Manage users", "Gestion des utilisateurs"))
        
        self.html.a(-1, '?spot=locations', id='menu_Locations', cls='menu_item')
        self.html.text(0, ("Storage locations", "Espaces de stockage"))
           