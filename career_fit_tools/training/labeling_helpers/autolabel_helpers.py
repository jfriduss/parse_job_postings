# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:48:23 2023

@author: jonat_od7omk3
"""
import ast
from career_fit_tools.misc_code.text_partitioning import case_insensitive_find


def get_mode_a_sentence_dicts(jobs_dicts, word):
    '''
    
    '''
    #keeps tract of how to map the sentences that contain the word that 'suggests label i', back to where they occur in the 
    #'jobs_dicts'
    sentences_dicts = []
    
    #create list of dictionaries that indicate which sentences have the keyword, but aren't labelled yet, and how to map them
    #back to the 'jobs_dicts'
    for i in range(len(jobs_dicts)):
        for j in range(len(jobs_dicts[i]['sentences'])):
            case_insensitive_search = case_insensitive_find(jobs_dicts[i]['sentences'][j], word)
            
            if ((jobs_dicts[i]['labels'][j][0] == 'na') & (case_insensitive_search != -1) ):
                #question: on one hand, it would be better to store job_id, in that less likely to make mistakes, compared to 
                #stored the index in the list. But on the other hand, easier to use if store the index in the list...
                sentences_dicts.append({'s': jobs_dicts[i]['sentences'][j], 'index_jobs_dict': i,
                                        'index_within_ad_of_sentence': j }) 
    return sentences_dicts
    

def get_mode_b_sentence_dicts(jobs_dicts, percent, section):
    '''
    
    '''
    
    #keeps tract of how to map the sentences that contain the word that 'suggests label i', back to where they occur in the 
    #'jobs_dicts'
    sentences_dicts = []
    
    #create list of dictionaries that indicate which sentences have the keyword, but aren't labelled yet, and how to map them
    #back to the 'jobs_dicts'
    for i in range(len(jobs_dicts)):
        n_sentences = len(jobs_dicts[i]['sentences'])
        n_per_ad = int(n_sentences*percent*0.01)
        
        for j in range(n_sentences):
            if section == 0:
                if ( (jobs_dicts[i]['labels'][j][0] == 'na') & (j < n_per_ad) ):
                    #question: on one hand, it would be better to store job_id, in that less likely to make mistakes, compared to 
                    #stored the index in the list. But on the other hand, easier to use if store the index in the list...
                    sentences_dicts.append({'s': jobs_dicts[i]['sentences'][j], 'index_jobs_dict': i,
                                            'index_within_ad_of_sentence': j }) 
            if section == 1:
                if ( (jobs_dicts[i]['labels'][j][0] == 'na') & (j > (n_sentences - j)) ):
                    #question: on one hand, it would be better to store job_id, in that less likely to make mistakes, compared to 
                    #stored the index in the list. But on the other hand, easier to use if store the index in the list...
                    sentences_dicts.append({'s': jobs_dicts[i]['sentences'][j], 'index_jobs_dict': i,
                                            'index_within_ad_of_sentence': j }) 
                
    return sentences_dicts


def get_mode_one_indices():
    
    ind_should_be_assigned_label = input("Please open the file 'sentences_to_label.html' and then input a list "
                                 "with the indices of the sentences that should get the label.")

    try:
        # Safely evaluate the input string as a Python expression to get the list
        ind_should_be_assigned_label = ast.literal_eval(ind_should_be_assigned_label)
    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a valid list of numbers.")
    else:
        if not isinstance(ind_should_be_assigned_label, list):
            print("Invalid input. Please enter a valid list of numbers.")

    return [int(n) for n in ind_should_be_assigned_label]    
    
    
def get_mode_two_indices():
    
    max_and_list_to_omit_tuple = input("Please open the file 'sentences_to_label.html' and then input a tuple "
                                    "whose first entry is an integer, and whose next entry is a list of integers. "
                                    "The number in the first entry is the index of the last sentence that you checked "
                                    " and the list in the second entry are the indices that should NOT be labelled. "
                                    "For example, (6, [3,5]), indicates that sentences at 0, 1, 2, 4 and 6 should be "
                                    "labelled. ")    
    
    try:
        # Safely evaluate the input string as a Python expression to get the list
        max_val, list_inds_to_omit = ast.literal_eval(max_and_list_to_omit_tuple)    

    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a tuple with an integer and a list.")
        
    list_inds_to_omit = [int(n) for n in list_inds_to_omit]  
    
    return [n for n in range(max_val+1) if n not in list_inds_to_omit]


def find_index_by_key_value(list_of_dicts, key, value):
    '''
    list_of_dicts: list of dictionaries, all of whose keys are the same name, and the values of a given key are of the same type
    key, value : key-value pair that want to see if exists in one of the dictionaries in the list. If such a pair exists, the
        function returns the index of the dictionary that it occurs. Else it returns -1.
    '''
    
    #note: enumerate creates an iterator that *is not subscriptable* (to save memory) where each element contains
    #(index_in_list, element_in_list)
    for index, dictionary in enumerate(list_of_dicts):
        if key in dictionary and dictionary[key] == value:
            return index
    return -1