# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:10:42 2023

@author: jonat_od7omk3
""" 
from text_partitioning import partition_string, reconstruct_ad_w_bolded_skills
from training.labelingHelpers.predict_and_label_helpers import tok_sent_and_classify_toks
from training.labelingHelpers.predict_and_label_helpers import classify_sentences

from career_fit_tools.get_if_qualified_indicators_helpers import load_model
from career_fit_tools.get_if_qualified_indicators_helpers import get_entities_from_words_and_labels
from career_fit_tools.get_if_qualified_indicators_helpers import create_token_labels_fr_word_labels

def get_if_qualified_indicators(job_descr, use_sentence_classifier = 1, print_descr_w_predictions = 0):
    '''
    extracts entities that can be used to determine whether or not a candidate is qualified for the job
    described in the job description passed to the function. entities are extracted according to the 
    annotation guidelines in the repo *insert where in the repo they are stored, here*
    
    takes a job description as a string, and optionally, two arguments to indicate whether or not to (i) use
        the sentence classifier to pre-filter sentences prior to token classification, and (ii) whether or
        not to print the job description, color coded according to how the token classification model labelled
        the data
    
    steps: 
        - loads the models (if not already loaded)
        - breaks the job description into a list of sentences 
        - make predictions on the sentences
        - if the 'print_descr_w_predictions' string indiciates to print the color coded job description after making
            predictions, print the color coded job description
        - returns a list of lists, with FILL THIS IN HERE!
    
    - labels tokens (with or without the sentence classifier as a first step, depending on value of 'use_sentence_classifier')
    - if 'print_descr_w_predictions' == 1, prints the job posting, with the words colored according to their label
    - returns a list of the labelled entities, with...
    '''
    
    if (use_sentence_classifier == 1):
        
        sentence_class_mod, sentence_class_tok, \
            token_class_mod, token_class_tok = load_model(use_sentence_classifier)
        
    else: token_class_mod, token_class_tok = load_model(use_sentence_classifier)
    
    sentences, helpers = partition_string(job_descr)

    d = {'sentences': sentences, 'helpers': helpers, 'labels': []}

    total_words_and_labs = []

    if (use_sentence_classifier == 1):
        labels_on_sentences = classify_sentences(sentence_class_tok, sentence_class_mod, d['sentences'])
            
    i = 0        
    for s in sentences:
        
        if (use_sentence_classifier == 1):
            if (labels_on_sentences[i] == 1):
                words_and_labs = tok_sent_and_classify_toks(token_class_tok, token_class_mod, s)
                token_labels = create_token_labels_fr_word_labels(s, words_and_labs, token_class_tok)
                total_words_and_labs.extend(words_and_labs)
                d['labels'].append( token_labels )                
            
            else:
                d['labels'].append( [0, []] )
            
        if (use_sentence_classifier == 0): 
            words_and_labs = tok_sent_and_classify_toks(token_class_tok, token_class_mod, s)
            token_labels = create_token_labels_fr_word_labels(s, words_and_labs, token_class_tok)
            total_words_and_labs.extend(words_and_labs)
            d['labels'].append( token_labels )

        i += 1
            
    entities_to_extract = get_entities_from_words_and_labels(total_words_and_labs)

    if print_descr_w_predictions == 1:
        reconstruct_ad_w_bolded_skills(d, token_class_tok, mode = 0)
        
    return entities_to_extract