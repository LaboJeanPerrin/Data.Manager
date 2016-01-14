#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import sqlite3          # SQLite 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ==========================================================================
class DB:
    '''
    The Database class
    '''
    
    # ----------------------------------------------------------------------
    def __init__(self, dbname):
        '''
        Constructor
        
        Inputs:
            dbname (str) the database filename
        '''
        
        self.connection = sqlite3.connect(dbname)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    # ----------------------------------------------------------------------
    def single(self, req, *args):
        '''
        Single result request
        
        Inputs:
            req   (str) SQL request
            *args (...) Arguments to fill the request
            
        Output:
            Request result (tupple)
        '''

        self.cursor.execute(req, args)

        return self.cursor.fetchone()

    # ----------------------------------------------------------------------
    def multi(self, req, *args):
        '''
        Multiple results request
        
        Inputs:
            req   (str) SQL request
            *args (...) Arguments to fill the request
            
        Output:
            Request results (list of tupples)
        '''
        
        self.cursor.execute(req, args)

        return self.cursor.fetchall()

    # ----------------------------------------------------------------------
    def insert(self, table, **kwargs):
        '''
        Insert row request
        
        Inputs:
            table (str) Table to insert in
            *args (...) List of values to insert
            
        Output:
            None
        '''
        
        # Insert a row of data
        self.cursor.execute('INSERT INTO {0} ({1}) VALUES ({2})'.format(table, ','.join(kwargs.keys()), ','.join(['?']*len(kwargs))), list(kwargs.values()))
        
        # Save changes
        self.connection.commit()
        
    # ----------------------------------------------------------------------
    def delete(self, table, where, *args):
        '''
        Delete request
        
        Inputs:
            table (str) Table to delete from
            where (str) WHERE condition
            *args (...) Arguments to fill the request
            
        Output:
            None
        '''
                
        # Delete a row of data
        self.cursor.execute("DELETE FROM {0} WHERE {1}".format(table, where), args)
        
        # Save changes
        self.connection.commit()
        
    # ----------------------------------------------------------------------
    def update(self, table, key, value, where, *args, encode=True):
        '''
        Update request
        
        Inputs:
            req   (str) SQL request
            *args (...) Arguments to fill the request
            
        Output:
            Request results (list of tupples)
        '''
        
        # Manage strings
        if isinstance(value, str) and encode is True:
            value = "'{0}'".format(value)
                    
        # Manage Null values
        if value is None:
            value = 'NULL'
        
        # Update request
        self.cursor.execute("UPDATE {0} SET {1}={2} WHERE {3}".format(table, key, value, where), args)
        
        # Save changes
        self.connection.commit()
        
    # ----------------------------------------------------------------------
    def lastid(self, table, field='id'):
        
        self.cursor.execute("SELECT MAX({1}) AS m FROM {0}".format(table, field))
        res = self.cursor.fetchone()
        return res['m']