# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:07:35 2023

@author: jonat_od7omk3
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")        
        print("occurred when calling 'read_query' ")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        print("occurred when calling 'create_db_connection' ")
    return connection


def table_to_df(db, pw, q, cols):
    '''
    db is a str with the name of the database that querying (e.g. 'jobs_db')
    pw is a str with the database password
    q is a string that contains the the sql query  
    cols is a list of str's with the names of the table's columns, e.g. 
        cols = ["job_id", "loc_searched_city", "actual_city", "loc_searched_state", "title_searched", "title", "descr", "salary", "date"]
    '''
    
    from_db = []
    
#     print('table_to_df query about to be executed \n\n')
    
    try:
    
        connection = create_db_connection("localhost", "root", pw, db)
        results = read_query(connection, q)
    
        for result in results:
            result = list(result)
            from_db.append(result)

        df = pd.DataFrame(from_db, columns=cols)    
    
    except IndexError: #there aren't entries that fit the criteria
        return('error')
    
    except TypeError:
        return('error')
    
    return df  


def q_all(tbl):
    
    if(type(tbl) == str): 
        #PROBABLY CHANGE THE QUERY AND THEN REMOVE THIS!
        tbl = [tbl]   
        
    q = '''
        SELECT * 
        FROM {};'''.format(
            ', '.join(["{}".format(value) for value in tbl]))
        
    return q