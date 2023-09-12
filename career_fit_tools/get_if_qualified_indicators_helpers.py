# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:16:30 2023

@author: jonat_od7omk3
"""

from transformers import AutoTokenizer, AutoModelForTokenClassification
from training.ft_sentence_classification_helpers import CustomModel
import os

sentence_classification_model = None
token_classification_model = None

path_to_sentence_classification_m = os.environ.get('PATH2MODEL')


def load_model(use_sentence_classifier):
    global sentence_classification_model
    global token_classification_model
    
    if (use_sentence_classifier == 0):
        if token_classification_model is None:
            # Load and initialize the model the first time
            token_classification_model_name = "jfriduss/bert_for_job_descr_parsing"
            token_class_mod = AutoModelForTokenClassification.from_pretrained(token_classification_model_name)
            token_class_tok = AutoTokenizer.from_pretrained(token_classification_model_name)
            token_classification_model = (token_class_mod, token_class_tok)   

        return token_classification_model
        
    if (use_sentence_classifier == 1) :
        
        if sentence_classification_model is None:
            # Load and initialize the sentence classification model the first time
            sentence_class_mod = CustomModel("has-abi/distilBERT-finetuned-resumes-sections", num_labels = 2)

            # p2model = "./model_contents/hf"
            # f_lin = "./model_contents/linear_layer_for_sent_classifier_fr_colab.pth"
            
            p2model = path_to_sentence_classification_m + 'hf'
            f_lin = path_to_sentence_classification_m + 'linear_layer_for_sent_classifier_fr_colab.pth'

            #overwriting it with weights from the google colab
            sentence_class_mod.overwrite_w_trained_weights(p2model, f_lin)
            #uploading the sentence classification tokenizer
            sentence_class_tok = AutoTokenizer.from_pretrained("has-abi/distilBERT-finetuned-resumes-sections")  
            sentence_classification_model = (sentence_class_mod, sentence_class_tok)   
        
        if token_classification_model is None:
            # Load and initialize the model the first time
            token_classification_model_name = "jfriduss/bert_for_job_descr_parsing"
            token_class_mod = AutoModelForTokenClassification.from_pretrained(token_classification_model_name)
            token_class_tok = AutoTokenizer.from_pretrained(token_classification_model_name)
            token_classification_model = (token_class_mod, token_class_tok)               
        
        
        return sentence_classification_model[0], sentence_classification_model[1], \
            token_classification_model[0], token_classification_model[1]


def get_entities_from_words_and_labels(input_list):
    result = []
    current_group = ''
    
    i = 0
    for item in input_list:
        text, value = item
        if value == 0:
            if len(current_group) != 0:
                result.append(current_group)
                current_group = text
            
            else: current_group = text
            
        if value == 1:                
            current_group += ' ' + text
        
        i += 1
        
        if ( (i == len(input_list)) & (len(current_group) != 0) ):
            result.append(current_group)
        
    return result


def create_token_labels_fr_word_labels(s, words_and_labels, tokenizer):
    '''
    takes words and labels that are aligned with the words, and outputs
    [1, labels_aligned_w_tokens], where the '1' out front is to indicate
    there are tokens to extract from the sentence
    '''
    
    sent_enc = tokenizer(s, padding = False, truncation = False, return_tensors="pt")
    word_ids = sent_enc.word_ids()

    token_index = 0
    label_index = 0

    w_id_prev = -1

    token_labels = ['na'] * len(word_ids)
    
    for w_id in word_ids: #continue here, making sure this part works as expected

        if w_id == None: token_labels[token_index] = -100

        elif ( (w_id == w_id_prev) | (w_id_prev == None) ):
            token_labels[token_index] = words_and_labels[label_index][1]

        else:
            label_index += 1
            token_labels[token_index] = words_and_labels[label_index][1]

        w_id_prev = w_id

        token_index += 1        
    
    return [1, token_labels ]


def get_symetric_diff(list1, list2):
    '''
    takes two lists, and returns the elements only in list1, only in list2, and
    the symetric difference of the two lists (treating the lists like a set/
    ignoring repeats)
    '''
    set1 = set(list1)
    set2 = set(list2)
    
    # Find elements in list1 that are not in list2
    elements_only_in_list1 = set1 - set2
    
    # Find elements in list2 that are not in list1
    elements_only_in_list2 = set2 - set1
    
    # Combine both sets to get the symmetric difference
    symmetric_difference = elements_only_in_list1.union(elements_only_in_list2)
    
    # Convert the result back to a list if needed
    result_list = list(symmetric_difference)
    
    # return the results
    print("Elements only in list1:", elements_only_in_list1)
    print('\n')
    print("Elements only in list2:", elements_only_in_list2)
    print('\n')
    print("Symmetric difference:", result_list)
    
    return elements_only_in_list1, elements_only_in_list2, result_list
    