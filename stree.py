#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
import subprocess
import difflib

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --------------------------------------------------------------------------
def run(cmd, parse=True, dlm='\n'):
    '''
    Run shell command .
    
    Inputs:
        - cmd   (str)       The command to execute
        - parse (bool=True) Parse the output
        - dlm   (str='\n')  Parsing delimiter
        
    Output:
        The command result.
    '''
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if parse:
        return out.decode().strip().split(dlm)
    else:
        return out.decode()
    
# --------------------------------------------------------------------------
def hsize(num, suffix='B'):
    '''
    Human-readable size
    '''
    
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

# --------------------------------------------------------------------------
def explore(L, pid):
    '''
    Directory exploration.
    
    Inputs:
        - L     (list)  The list
        - pid   (int)   The parent identifier
        
    Outputs:
        - L     (list)  The modified list
    '''
    
    print()
    print(L)
    
    root = L[pid][3]
    psize = 0
    
    dext = {}
    res = run("ls -qgGd \"{0}\"/* | awk '{{d=substr($1,0,1);s=$3; $1=$2=$3=$4=$5=$6=\"\";gsub(/^[ ]+/, \"\", $0);print d,s,substr($0,{1},256)}}'".format(root, len(root)+2))
    for r in res:
        
        print(r)
        
        # Definitions
        tmp = r.split()
        isdir = tmp[0]=='d'
        
        if isdir:
            
            # ===================================
            #   DIRECTORY
            # ===================================
            
            # --- Add directory to list
            L.append([pid, 0, None, root+'/'+' '.join(tmp[2:])])
            id = len(L)-1
            
            # --- Recursive exploration
            L = explore(L, id)
            
            # --- Update parent size
            psize += L[id][2]
            
        else:
            
            # ===================================
            #   FILES
            # ===================================

            # --- Definitions
            size = int(tmp[1])
            fname = tmp[2]
            _, ext = os.path.splitext(tmp[2])
            ext = ext[1:]
            
            # --- Sort by extension
            if ext in dext:
                
                dext[ext]['n'] += 1
                dext[ext]['size'] += size
                
                # Update pattern
                SM = difflib.SequenceMatcher(None, dext[ext]['pattern'], fname)
                blocks = SM.get_matching_blocks()
                b1 = None
                b2 = None
                for B in blocks:
                    bs = fname[B.b:B.b+B.size]
                    if not bs.isdigit():
                        if b1 is None:
                            b1 = bs
                        elif b2 is None:
                            b2 = bs
                            break
                dext[ext]['pattern'] = b1 + '*' + b2
                
                # Number of digits
                nrc = len(fname)-len(b1)-len(b2)
                if dext[ext]['mind'] is None or nrc<dext[ext]['mind']:
                    dext[ext]['mind'] = nrc
                if dext[ext]['maxd'] is None or nrc>dext[ext]['maxd']:
                    dext[ext]['maxd'] = nrc
                
            else:
                dext[ext] = {'n': 1, 'size': size, 'pattern': fname, 'mind': None, 'maxd': None}
            
    # --- Append files to the list
    for ext, X in dext.items():
        L.append([pid, X['n'], X['size'], X['pattern']])
        psize += X['size']
            
    # --- Update parent foler size
    L[pid][2] = psize
            
    return L

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Clear the screen
os.system('clear')

# --- Inputs
root = str(sys.argv[1])

L = [[None, 0, None, root]]
L = explore(L, 0)

# --- Display
        
for i, x in enumerate(L):
    
    out = ''
    
    # --- Find level
    lvl = 0
    parent = x[0]
    while parent is not None:
        parent = L[parent][0]
        lvl += 1
    
    # --- Level spacers
    if lvl>0:
        
        if x[0] in [item[0] for item in L[i+1:]]:        
            out += ' │ '*(lvl-1) + ' ├─'
        else:
            out += ' │ '*(lvl-1) + ' └─'
    
    # --- Size on disk
    tmp = '[' + hsize(x[2]) + ']'
    out += tmp + ' '*(10-len(tmp))
    
    # --- Name
    if x[0] is None:
        out += '    ' + x[3]
    else:
        if x[1]==0:     # Directory
            out += '    \033[1m' + x[3][len(root)+1:] + '\033[0m'
            
        elif x[1]==1:   # File
            out += '    \033[34m' + x[3] + '\033[0m'
            
        else:           #Group
            out += '    \033[31m' + x[3] + '\033[0m [' + str(x[1]) + ' files]'
    
    print(out)
