#!/usr/bin/python3
# -*-coding:UTF-8 -*

__version__ = 'v1.2.3'

'''
To do:

* With -b, ensure that the number of characters is the same for the size in all lines
* -m option (indicate average file size for groups)

'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
import argparse
import subprocess
import re
import json

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
    
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

# --------------------------------------------------------------------------
def bsize(num, suffix=' B'):
    '''
    Size in bytes
    '''

    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % num)+suffix

# ==========================================================================
class STree:
    """
    The STree class
    
    """
    
    # ----------------------------------------------------------------------
    def __init__(self, progress=False):
        '''
        STree constructor
        '''
        
        # --- Initialisation
        self.L = []
        self.progress = progress
        self.stats = {'folders':0, 'files': 0}
        self.tsize = 0

    # ----------------------------------------------------------------------
    def explore(self, root=None, pid=0):
        '''
        Directory exploration.
        
        Inputs:
            - pid=0     (int)   The parent identifier
            
        Outputs:
            None
        '''
        
        # Initialization
        psize = 0
        dext = {}
        
        # Definitions
        if root is None:
            root = self.L[pid][4]
        else:
            self.L = [[None, 0, None, root, root]]
        
        # Get elements list
        res = run("ls -qgG \"{0}\" | awk -f {1}/stree.awk".format(root, os.path.dirname(os.path.realpath(__file__))))
        
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
                if len(ext)==0:
                    idext = '.'
                else:
                    idext = ext[1:]
                    
                # --- Sort by extension
                if idext in dext: 
                    
                    dext[idext]['n'] += 1
                    dext[idext]['size'] += size
                    
                    # --- Recognize patterns
                    
                    # Prefix pattern
                    if dext[idext]['p1'] is not '':
                        i = 0
                        while dext[idext]['p1'][i]==name[i]:
                            i+=1
                            if i==len(dext[idext]['p1']) or i==len(name):
                                break;
                        
                        if i==0:
                            dext[idext]['p1'] = ''
                        else:
                            dext[idext]['p1'] = dext[idext]['p1'][:i]
                    
                    # Suffix pattern
                    if dext[idext]['p2'] is not '':
                        i = 0
                        while dext[idext]['p2'][i]==name[-i-1]:
                            i+=1
                            if i==len(dext[idext]['p2']) or i==len(name):
                                break;
                        
                        if i==0:
                            dext[idext]['p2'] = ''
                        else:
                            dext[idext]['p2'] = dext[idext]['p2'][:i]
                    
                    # Update max name size
                    if len(name)>dext[idext]['max']:
                        dext[idext]['max'] = len(name)
                    
                else:
                    dext[idext] = {'n': 1, 'size': size, 'p1': name, 'p2': name[::-1], 'max': len(name)}
                
                # --- Update stats
                self.stats['files'] += 1
                self.tsize += size
                
            else:
                
                # ===================================
                #   DIRECTORY, LINK
                # ===================================
                
                # --- Add directory to list
                if etype=='d':
                    self.L.append([pid, 0, None, name, root + '/' + name])
                elif etype=='l':
                    ntmp = name.split(' -> ')
                    self.L.append([pid, -1, None, ntmp[0], ntmp[1]])
                id = len(self.L)-1
                
                # --- Update progress
                if self.progress:
                    print('folder:', root + '/' + name)
                    sys.stdout.flush()
                
                # --- Recursive exploration
                self.explore(pid=id)
                
                # --- Update stats
                self.stats['folders'] += 1
                
                # --- Update parent size
                if etype=='d':
                    psize += self.L[id][2]
                
        # --- Append files to the list
        for _, X in dext.items():
            if X['n']==1:
                pattern = X['p1']
            else:
                pattern = X['p1'] + '*'*(X['max']-len(X['p1']+X['p2'])) + X['p2'][::-1]
            self.L.append([pid, X['n'], X['size'], pattern, pattern])
            psize += X['size']
                
        # --- Update parent foler size
        self.L[pid][2] = psize
        
        # --- Update progress
        if self.progress:
            print('stat:', self.stats['files'], hsize(self.tsize))
            sys.stdout.flush()
                
    # ----------------------------------------------------------------------
    def load_json(self, filename):
        '''
        Load json file
        '''
        
        f = open(filename, 'r')
        self.L = json.load(f)
        f.close()
    
    # ----------------------------------------------------------------------
    def build(self, media='shell'):
        '''
        Build display.
        
        Inputs:
            - L     (list)  The list
            
        Outputs:
            - out   (str)   The string for display
        '''
        
        out = ''
        
        for i, x in enumerate(self.L):
            
            # --- Find level
            
            pre = ''
            parent = x[0]
            while parent is not None:
                if parent in [item[0] for item in self.L[i+1:]]:
                    if parent is x[0]:
                        pre += '─├ '
                    else:
                        pre += ' │ '
                else:
                    if parent is x[0]:
                        pre += '─└ '
                    else:
                        pre += '   '
                parent = self.L[parent][0]
            out += pre[::-1]
            
        
        
            
            # --- Size on disk
            if args.bytes:
                tmp = '[' + bsize(x[2]) + ']'
                out += tmp
            else:
                tmp = '[' + hsize(x[2]) + ']'
                out += tmp + ' '*(10-len(tmp))
            
            # --- Name
            if x[1]==-1:     # Link
                if media=='shell':
                    out += '    \033[1m\033[32m' + x[3] + '\033[0m -> ' + x[4]
                elif media=='html':
                    out += '    <span style="color:#6F0; font-weight: bold;">' + x[3] + '</span> -> ' + x[4]
            
            elif x[1]==0:     # Directory
                if media=='shell':
                    out += '    \033[1m' + x[3] + '\033[0m'
                elif media=='html':
                    out += '    <b>' + x[3] + '</b>'
                    
            elif x[1]==1:   # File
                if media=='shell':
                    out += '    \033[34m' + x[3] + '\033[0m'
                elif media=='html':
                    out += '    <span style="color:#36C;">' + x[3] + '</span>'
            else:           #Group
                if media=='shell':
                    out += '    \033[36m' + x[3] + '\033[0m [' + str(x[1]) + ' files]'
                elif media=='html':
                    out += '    <span style="color:#399;">' + x[3] + '</span> [' + str(x[1]) + ' files]'
                    
            out += '\n'
                    
        # --- Special HTML wrapping
        if media=='html':
            
            out = '<!doctype html><html><head><meta charset="utf-8"><title>Smart tree</title></head><body><pre style="font-size:10pt;">' + out + '</pre></body></html>'
                    
        return out


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Clear the screen
# os.system('clear')

# --- Inputs ---------------------------------------------------------------

parser = argparse.ArgumentParser(description='Smart tree')
parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")
parser.add_argument("root", nargs='+', help="The smart tree root")
parser.add_argument("-b", "--bytes", action="store_true", help="Display bytes intead of human readable sizes")
parser.add_argument("-i", "--input", help="Input file")
parser.add_argument("-o", "--output", help="Output file")
parser.add_argument("-p", "--progress", action="store_true", help="Progress information")
args = parser.parse_args()

# --- Computation ----------------------------------------------------------

ST = STree(progress=args.progress)

if args.input is None:
    
    ST.explore(root=' '.join(args.root))
       
else:
    
    ST.load_json(args.input)
    

# --- Outputs --------------------------------------------------------------

if args.output is None:

    # -------------------------------------------
    #    DISPLAY OUTPUT
    # -------------------------------------------

    print()
    print(ST.build())
    print()
    
else:
    
    # -------------------------------------------
    #   FILE OUTPUT
    # -------------------------------------------
    
    # --- Check extension
    name, ext = os.path.splitext(args.output)
    
    if ext=='.html':
        
        s = ST.build(media='html')
        with open(args.output, "wt") as out_file:
            out_file.write(s)
        
    else:
        
        f = open(args.output, 'w+')
        json.dump(ST.L, f)
        f.close()
