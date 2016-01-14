#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import cgi, cgitb       # CGI
import importlib        # Dynamic import (pages import)
import sys

from Snippets.settings import get_settings
from Snippets.sessions import get_session
from Snippets.data import get_data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    INITIALIZATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --- Definitions
inputs = cgi.FieldStorage()
settings = get_settings()
data = get_data()
session = get_session(inputs, settings, data)

# --- Html header
print(session.cookie)
print("Content-Type: text/html;charset=utf-8\n")

# --- Debugging
cgitb.enable()

# --- Get page name
if session.user is None:
    spot = 'connection'
else:
    spot = inputs.getvalue('spot')
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CREATE PAGE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --- Import page module

try:
    Spot = importlib.import_module('Spots.{0}'.format(spot))
    settings.set('spot', spot)
    
except ImportError:
    Spot = importlib.import_module('Spots.error')
    settings.set('spot', 'error')
    
# --- Create spot
S = Spot.spot(settings, session, data, inputs)

# --- Display
if S.display:
    print(S.html.build())
