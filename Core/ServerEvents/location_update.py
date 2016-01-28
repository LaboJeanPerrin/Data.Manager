#!/usr/bin/python3
# -*-coding:UTF-8 -*

# --------------------------------------------------------------------------
#   IMPORTS
# --------------------------------------------------------------------------

import sys
import subprocess
import cgi

# --------------------------------------------------------------------------
#   FUNCTIONS
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
def send(s, what='data'):
    sys.stdout.write('{0}:{1}\n\n'.format(what, s))
    sys.stdout.flush()

# --------------------------------------------------------------------------
#   CONNECTION
# --------------------------------------------------------------------------

# --- Html header
send('text/event-stream;charset=utf-8', what='Content-type')
send('3600000', what='retry')

# --- Inputs
inputs = cgi.FieldStorage()
IP = inputs.getvalue('ip')
path = inputs.getvalue('path')
name = inputs.getvalue('name')
jpath = inputs.getvalue('jpath').strip()


'''
send('Test')
send(''.join(['&%d;' % ord(x) for x in 'Poisson n°1']))
send('!CLOSE')
'''

if IP is not None:

    # --- STREE CONSTRUCTION -----------------------------------------------
    cmd = "ssh -t -t ljp@{0} 'python3 /home/ljp/.stree/stree.py -p \"{1}\" -o \"/home/ljp/.stree/Trees/{2}.json\"'".format(IP, path, name)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # --- Subprocess monitoring
    for line in iter(p.stdout.readline, b''):
        tmp = ''.join(['&#%d;' % ord(x) for x in line.rstrip().decode(encoding='UTF-8')])
        send(tmp)
        # send(line.rstrip().decode(encoding='UTF-8'))

    # --- STREE IMPORT -----------------------------------------------------
    
    # --- Import JSON file
    send('!IMPORT')
    
    # --- Subprocess preparation
    cmd = "scp ljp@{0}:\"'/home/ljp/.stree/Trees/{1}.json'\" '{2}'".format(IP, name, jpath)
    send(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # --- Subprocess monitoring
    for line in iter(p.stdout.readline, b''):
        send(line.rstrip().decode(encoding='UTF-8'))
    
    # --- END --------------------------------------------------------------
    send('!CLOSE')
