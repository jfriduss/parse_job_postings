# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:32:49 2023

@author: jonat_od7omk3
"""
from .autolabel_helpers import get_mode_a_sentence_dicts, get_mode_b_sentence_dicts
from .autolabel_helpers import get_mode_one_indices, get_mode_two_indices
from .autolabel_helpers import find_index_by_key_value
from text_partitioning import replace_substring
import random


def autolabel(jobs_dicts, word, label, percent = 5 , section = 0, related_words = []):
    '''
    Takes the list of dictionaries, a keyword, the label assigned to that keyword, and a list of 
    keywords from another field. The keyword is used to label sentences with that keyword with 
    the appropriate label, and the list of keywords is used to data augmentation.
        Note: it outputs an html file for the user to look through and choose the sentences that should get
        the label, so that, if some word occurs in a context that it has a different meaning, the user can
        identify that and not label the sentence with that label
    '''
    
    mode_sentence = input("Which mode for choosing what sentences to label would you "
                          "like to use ('word' or 'first_and_last_sentences')?")
    
    while (mode_sentence != 'word') & (mode_sentence != 'first_and_last_sentences'):
        mode = input("Please enter either 'word' or 'first_and_last_sentences'. ")

    #'sentences_dicts' keeps tract of how to map the sentences that contain the word that 'suggests label i', back 
    #to where they occur in the 'jobs_dicts'
    
    if mode_sentence == 'word':
        sentences_dicts = get_mode_a_sentence_dicts(jobs_dicts, word)
    
    if mode_sentence == 'first_and_last_sentences':
        sentences_dicts = get_mode_b_sentence_dicts(jobs_dicts, percent, section)    
    
    #create html file with sentences and indices, so that can have that on a different monitor while inputting the list into
    #the console on this monitor
    
    html_sentences_and_indices = ''
    
    #if only show 'index_job_id' to the user, issues arise if the word shows up in multiple sentences in the job ad. 
    #if show both 'index_job_ad' and 'index within sentence', then have to search through two different lists, most of the time
    #this dict addresses both of those
    map_fr_ind_to_sentences_ind = {}
    
    for k in range(len(sentences_dicts)):
        sd = sentences_dicts[k]
        map_fr_ind_to_sentences_ind[k] = (sd['index_jobs_dict'], sd['index_within_ad_of_sentence'])
        #want to show the user the index in the *jobs_dict* that the sentence appears...what happens if two sentences in a
        #job ad have, for example, SQL in them? To mitigate, make this a tuple instead, with (k, sd['index_jobs_dict'])
        html_sentences_and_indices += "<b>" + str(k) + "</b> "
        html_sentences_and_indices += sd['s']
        html_sentences_and_indices += '<br>'
        k += 1
        
    with open("sentences_to_label.html", "w", encoding='utf-8') as file:
        file.write(html_sentences_and_indices)    
    
    
    mode = input("Which mode would you like to use ('normal' or 'max_and_indices_to_omit')?")
    
    while (mode != 'normal') & (mode != 'max_and_indices_to_omit'):
        mode = input("Please enter either 'normal' or 'max_and_indices_to_omit'. ")

    if mode == 'normal':
        ind_should_be_assigned_label = get_mode_one_indices()
    
    if mode == 'max_and_indices_to_omit':
        ind_should_be_assigned_label = get_mode_two_indices()
    
    #START data augmentation portion1, make use_data_aug True when have the POS tagger figured out!
    
    use_data_aug = False
    
    if use_data_aug & (mode_sentence == 'word'):
    
        created_sentences  = [] #unlike most other lists, this is just a list of sentences
        n_related_words_to_choose = int(len(related_words)/3)


        for ind in ind_should_be_assigned_label:
            #choose some words for data augmentation
            i_job_dict, i_within_ad_of_sentence = map_fr_ind_to_sentences_ind[ind]
            labelled_sentence = jobs_dicts[i_job_dict]['sentences'][i_within_ad_of_sentence]
            words_for_data_aug = random.sample(related_words, n_related_words_to_choose)
            created_sentences.extend( [replace_substring(labelled_sentence, word, data_aug_word)
                                       for data_aug_word in words_for_data_aug]  )        
    
    #not data aug stuff
    for ind in ind_should_be_assigned_label:
        ind_job_dict = map_fr_ind_to_sentences_ind[ind][0]
        ind_within_sentence = map_fr_ind_to_sentences_ind[ind][1]
        jobs_dicts[ind_job_dict]['labels'][ind_within_sentence][0] = label    
    
    
    #add sentences and labels to the 'data augmentation dictionary'. Will have it have the key str(10**6) = '1000000', so that 
    #all keys are still able to easily be converted to ints, but I am unlikely to scrape a million job ads!
    
    #START data augmentation portion1, un comment when have the POS tagger figured out!    
    #get the data augmentation dictionary index, if it exists. NEED TO CHANGE THE STRUCTURE OF 
    #THE DICTIONARY THAT APPENDING, TO CONFORM TO NEW APPROACH (only do this if actually end up
    #using data augmentation though)
    
    if use_data_aug & (mode_sentence == 'word'):
        data_aug_ind = find_index_by_key_value(jobs_dicts, 'job_id', 10**6)

        if data_aug_ind != -1:
            jobs_dicts[data_aug_ind]['sentences'].extend(created_sentences)
            jobs_dicts[data_aug_ind]['labels'].extend([label]*len(created_sentences))

        else:
            d_data_augm = { 'job_id' : (10**6), 'sentences': created_sentences, 'labels': [label]*len(created_sentences)  }
            jobs_dicts.append(d_data_augm)

    #END data augmentation portion1, un comment when have the POS tagger figured out!    
        
    return jobs_dicts


