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

# --- Inputs
inputs = cgi.FieldStorage()
IP = inputs.getvalue('ip')
path = inputs.getvalue('path')
jpath = inputs.getvalue('jpath')

if IP is not None:

    # --- Subprocess preparation
    cmd = "sshpass -p ljp3231 ssh -t -t ljp@{0} 'python3 /home/ljp/.stree/stree.py -p {1} -o {2}'".format(IP, path, jpath)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # --- Subprocess monitoring
    for line in iter(p.stdout.readline, b''):
        send(line.rstrip().decode(encoding='UTF-8'))

    send('!CLOSE')
