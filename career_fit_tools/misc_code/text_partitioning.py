# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:14:37 2023

@author: jonat_od7omk3
"""
import re
from career_fit_tools.training.labeling_helpers.predict_and_label_helpers import group_tuples_by_first_index

def partition_string(input_string):
    sentences = re.split(r'(?<=[.!?])\s+|\n', input_string)

    helper = create_helper(input_string, sentences)
    
    return sentences, helper


def replace_substring(str_main, str_to_replace, replacement_str):
    '''
    takes three strings, str_main, a substring of str_main, str_to_replace, and a third string, replacement_str 
    and returns a string that is str_main, except with replacement_str in the position where str_to_replace was
    '''
    index = case_insensitive_find(str_main, str_to_replace)
    
    if index == -1:
        # If the substring to be replaced is not found, return the original string
        return str_main
    
    # Construct the modified string
    result = str_main[:index] + replacement_str + str_main[index + len(str_to_replace):]
    return result


def case_insensitive_find(main_string, sub_string):
    '''
    find where a substring occurs within a larger string, except in contrast to python's version, this one is 
    case insensitive
    '''
    main_lower = main_string.lower()
    sub_lower = sub_string.lower()
    return main_lower.find(sub_lower)


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


def reconstruct_ad_w_bolded_skills(d, tok, mode = 0):
    sentences = d['sentences']
    recr_posting = d['helpers']
    labels = d['labels']
    
    if mode == 0:
        #the ad has been hand annotated
        i = 1
        for s in sentences: 
            #there isn't something to bold in this sentence
            str_to_repl = '[' + str(i) + ']'
            
            if labels[i-1][0] == 0:
                recr_posting = case_insensitive_replace_substring(recr_posting, str_to_repl, s)
            
            elif labels[i-1][0] == 1:
                #there is something to bold in this sentence
                s_bolded = bold_skills_within_sentence(s, labels[i-1], tok, 1)
                recr_posting = case_insensitive_replace_substring(recr_posting, str_to_repl, s_bolded)
                
            i += 1       
        
        print(recr_posting)
        
    elif mode == 1:
        #the ad has not been annotated, and predictions will be made to determine which words are bolded
        pass
    
    
def bold_skills_within_sentence(sentence, labels, tokenizer, ret_or_print):
    '''
    document this. explain how it is similar, but different, than the 'label_skills_in_sentence_and_print' fcn
    '''
        
    tok_sent_obj = tokenizer(sentence, padding = False, truncation = False, return_tensors="pt")
    
    helper_l = list(zip(tok_sent_obj.tokens(), tok_sent_obj.word_ids(), labels[1] ))
    helper_l = [el for el in helper_l if el[1] != None]    

    grouped_helper_l = group_tuples_by_first_index(helper_l)
    
    results = []
    
    for sublist in grouped_helper_l:
        concatenated_string = ''    

        for tup in sublist:
            concatenated_string += tup[0].replace('##', '')        
        results.append((concatenated_string, sublist[0][2]))
    
    bolded_s = ''
    i = 0
    for r in results:
        if (r[1] == 2): bolded_s += r[0]
        elif (r[1] == 0): bolded_s += "\033[35;5;9m" + r[0] + "\033[0m" #purple
        elif (r[1] == 1): bolded_s += "\033[33;5;9m" + r[0] + "\033[0m" #yellow
        bolded_s += ' '        
        i += 1
        
    if ret_or_print == 0:    
        print(bolded_s)
    elif ret_or_print == 1:    
         return bolded_s        