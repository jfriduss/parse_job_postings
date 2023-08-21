# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:14:37 2023

@author: jonat_od7omk3
"""
import re


def partition_string(input_string):
    sentences = re.split(r'(?<=[.!?])\s+|\n', input_string)

    helper = create_helper(input_string, sentences)
    
    return sentences, helper


def case_insensitive_replace_substring(str_main, str_to_replace, replacement_str):
    '''
    takes three strings, str_main, a substring of str_main, str_to_replace, and a third string, replacement_str 
    and returns a string that is str_main, except with replacement_str in the position where str_to_replace was
    '''
    index = str_main.find(str_to_replace)
    
    if index == -1:
        # If the substring to be replaced is not found, return the original string
        return str_main
    
    # Construct the modified string
    result = str_main[:index] + replacement_str + str_main[index + len(str_to_replace):]
    return result


def create_helper(input_string, sentences):
    i = 1
    for s in sentences:
        repl_str = '[' + str(i) + ']'
        input_string = case_insensitive_replace_substring(input_string, s, repl_str )
        i += 1
    return input_string

def reconstruct_description(sentences, helper):
    i = 1
    for s in sentences:
        str_to_repl = '[' + str(i) + ']'
        helper = case_insensitive_replace_substring(helper, str_to_repl, s)
        i += 1
    return helper