# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:07:35 2023

@author: jonat_od7omk3
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd
import json


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


def open_json_safe(file_name):
    '''
    Takes the name of the json file with the list of dicts, and makes sure the user has saved the information
    in the list of dicts, before opening it. Also, converts job id's to ints.
    '''
    user_input = input("When you run this function, you might overwrite the data in the data structure in python that you are "
                    "labelling. Are you sure you want to run it? (y/n): ")
    
    while user_input.lower() not in ['y', 'n']:
        print("Invalid input. Please enter 'y' to continue or 'n' to exit.")    
    
    if user_input.lower() == 'y':
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        #bc json files can't save ints, need to convert the job ids back to ints
        for d in data:
            d['job_id'] = int(d['job_id'])
                
        return data 
    
    else:
        print('No data structure was returned')


def save_json_file(list_of_dicts, file_name):
    
    user_input = input("Are you sure you want to save the json file? "
                    "If you by mistake save it when you are just testing stuff "
                    "it might be a pain to fix? (y/n): ")
    
    while user_input.lower() not in ['y', 'n']:
        print("Invalid input. Please enter 'y' to continue or 'n' to exit.")      
    
    if user_input.lower() == 'y':    
        for d in list_of_dicts:
            d['job_id'] = str(d['job_id'])
            
        list_of_dicts_json = json.dumps(list_of_dicts)
        with open(file_name, 'w') as f:
            f.write(list_of_dicts_json)

    else:
        print('The json file was not updated and saved.')   