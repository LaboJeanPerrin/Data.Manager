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
    
    # Initialization
    psize = 0
    dext = {}
    
    # Definitions
    root = L[pid][4]
    
    # Get elements list
    res = run("ls -qgG \"{0}\" | awk -f stree.awk".format(root))
    
    for r in res:
    
        # --- Skip empty folders
        if r=='':
            continue
             
        # --- Definitions
        tmp = r.split()
        etype = tmp[0]
        name = ' '.join(tmp[2:])
        
        if etype=='-':
        
            # ===================================
            #   FILE
            # ===================================

            # --- Definitions
            size = int(tmp[1])
            _, ext = os.path.splitext(name)
            ext = ext[1:]
            
            # --- Sort by extension
            if ext in dext:
                
                dext[ext]['n'] += 1
                dext[ext]['size'] += size
                
                # Update pattern
                SM = difflib.SequenceMatcher(None, dext[ext]['p1']+dext[ext]['p2'], name)
                blocks = SM.get_matching_blocks()
                p1 = None
                p2 = None
                for B in blocks:
                    bs = name[B.b:B.b+B.size]
                    if not bs.isdigit():
                        if p1 is None:
                            p1 = bs
                        elif p2 is None:
                            p2 = bs
                            break
                dext[ext]['p1'] = p1
                dext[ext]['p2'] = p2
                
                # Number of digits
                nrc = len(name)-len(p1)-len(p2)
                if dext[ext]['maxd'] is None or nrc>dext[ext]['maxd']:
                    dext[ext]['maxd'] = nrc
                
            else:
                dext[ext] = {'n': 1, 'size': size, 'p1': name, 'p2': '', 'maxd': None}
            
        else:
            
            # ===================================
            #   DIRECTORY, LINK
            # ===================================
            
            # --- Add directory to list
            if etype=='d':
                L.append([pid, 0, None, name, root + '/' + name])
            elif etype=='l':
                ntmp = name.split(' -> ')
                L.append([pid, -1, None, ntmp[0], ntmp[1]])
            id = len(L)-1
            
            # --- Recursive exploration
            L = explore(L, id)
            
            # --- Update parent size
            if etype=='d':
                psize += L[id][2]
        
    # --- Append files to the list
    for ext, X in dext.items():
        if X['maxd'] is None:
            pattern = X['p1']
        else:
            pattern = X['p1'] + '\033[31m' + '*'*X['maxd'] + '\033[36m' + X['p2']
        L.append([pid, X['n'], X['size'], pattern, pattern])
        psize += X['size']
            
    # --- Update parent foler size
    L[pid][2] = psize
            
    return L

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Clear the screen
# os.system('clear')
print()

# --- Inputs
root = str(sys.argv[1])

L = [[None, 0, None, root, root]]
L = explore(L, 0)

# --- Display
for i, x in enumerate(L):
    
    out = ''
    
    # --- Find level
    
    pre = ''
    parent = x[0]
    while parent is not None:
        if parent in [item[0] for item in L[i+1:]]:
            if parent is x[0]:
                pre += '─├ '
            else:
                pre += ' │ '
        else:
            if parent is x[0]:
                pre += '─└ '
            else:
                pre += '   '
        parent = L[parent][0]
    out += pre[::-1]
    
    
    # --- Size on disk
    tmp = '[' + hsize(x[2]) + ']'
    out += tmp + ' '*(10-len(tmp))
    
    # --- Name
    if x[0] is None:
        out += '    ' + x[3]
    else:
        if x[1]==-1:     # Link
            out += '    \033[1m\033[32m' + x[3] + '\033[0m -> ' + x[4]
        
        elif x[1]==0:     # Directory
            out += '    \033[1m' + x[3] + '\033[0m'
            
        elif x[1]==1:   # File
            out += '    \033[34m' + x[3] + '\033[0m'
            
        else:           #Group
            out += '    \033[36m' + x[3] + '\033[0m [' + str(x[1]) + ' files]'
    
    print(out)
    
print()