# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 18:06:47 2023

@author: jonat_od7omk3
"""
from text_partitioning import reconstruct_ad_w_bolded_skills
import ast

from training.labelingHelpers.predict_and_label_helpers import html_w_labs_and_num_align_to_word

def after_labelling(d, token_class_tok, n_unsure):
    '''
    This function is used when creating new annotation guidelines, or when the current ones are in flux. 
    
    It takes:
        - a dictionary that has job description information and sentence/token labelling done on the
    description
        - the tokenizer used to tokenize the sentences for token classification
        - the number of words that it was unclear whether or not to annotate them. 
    
    It outputs, of the words that were annotated, the percentage that the annotator considered the guidelines
    to note dictate unambiguosly whether or not they should be annotated, as well as the reconstructed ad, with
    the words color coded according to label.
    '''
    n_words_annotated = 0
    
    for i in range(len(d['labels'])):
        for j in range(len(d['labels'][i][1])):
            if ((d['labels'][i][1][j] == 0) | (d['labels'][i][1][j] == 1)): n_words_annotated += 1
    
    
    perc_unsure = (100 - (100*n_unsure/n_words_annotated))
    print("The percentage of annotated tokens that it was unclear whether or not to annotate them "
          "in this description is: " + str(perc_unsure) + "\n\n")
    
    reconstruct_ad_w_bolded_skills(d, token_class_tok ,0)
    

def get_which_postings_are_labelled(list_of_dicts):
    has_labelled_sentences = []
    has_labelled_tokens = []
    
    i = 0
    
    for d in list_of_dicts:
        toks_labelled = 1
        for labels in d['labels']:
            tok_labs = [labs for labs in labels[1]]
    
            if (('na' in tok_labs) & ((labels[0] == 1) | (labels[0] == 'na') )): 
                toks_labelled = 0
    
        if (toks_labelled == 1) : has_labelled_tokens.append(i)

        sent_labs = [labs[0] for labs in d['labels']]
        if 'na' not in sent_labs:
            has_labelled_sentences.append(i)
            
        i += 1
    
    
    print('The sentences in the job descriptions stored at indices'
          ' ' + str(has_labelled_sentences) + ' are all labelled.\n')
    
    print('The sentences in the job descriptions stored at indices'
          ' ' + str(has_labelled_tokens) + ' have all their tokens '
          'labelled as well.')    


def reset_sentence_labels(d):
    for i in range(len(d['labels'])):
        d['labels'][i][0] = 'na'
    
    
def update_tokens_label(d, tokenizer_token_classification):

    '''
    This function takes a dictionary with information about the job description, in the same form used throughout the project:
        -keys: 'job_id', 'sentences', 'helpers', 'labels', where labels has both the sentence classification and NER labels
   
   It is used to correct mislabelled data, by taking the above dictionary and then..
   
        - outputting the sentences bolded if the model predicts it has relavent tokens, normal if not 
        - you indicate which sentences need have their label changed
        - those sentences labels are updated accordingly (because the sentence classifier has only two labels,
            those labels just get swapped)
        
        - then outputting the sentences with tokens that are labelled, colored according to label
        - you indicate which tokens need have their label changed, and what they should be changed to
        - those token labels are updated accordingly        
    '''
    
    #does the aspect of process described above, that pertains to creating labels for sentence classification
    update_tokens_label_sentences(d)
    
    #does the aspect of process described above, that pertains to creating labels for NER
    update_tokens_label_tokens(d, tokenizer_token_classification)
    

def update_tokens_label_sentences(d):
    '''
    This function does the portion involving making prediction on, and labelling the sentences of the job posting, 
    as part of the 'update_tokens_label' function. See the docustring of that function, for more information.
    '''
    
    #write sentences, and the indices in the d['sentences'] that they appear, to an html file
    #with sentences bolded if model predicts has relavent tokens and normal if not
    
    html_sentences_and_indices = "Black: 'Does not contain words to label'<br>Red: 'contains words to label'<br><br>"
    for i in range(len(d['sentences'])):
        html_sentences_and_indices += "<b>" + str(i) + "</b> "
        if (d['labels'][i][0] == 0): html_sentences_and_indices += d['sentences'][i]
        if (d['labels'][i][0] == 1): html_sentences_and_indices += "<span style=\"color: red;\">" + d['sentences'][i] + "</span>"
        html_sentences_and_indices += '<br>'
        
    with open("sentences_w_current_labels.html", "w", encoding='utf-8') as file:
        file.write(html_sentences_and_indices)     
        
    #asks human annotator to indicate which sentences were labelled incorrectly
    ind_mislabelled = input("Please open the file 'sentences_w_current_labels.html' and then input a list "
                                 "with the indices of the sentences that are labelled incorrectly.")

    try:
        # Safely evaluate the input string as a Python expression to get the list
        ind_mislabelled = ast.literal_eval(ind_mislabelled)
    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a valid list of numbers.")
    else:
        if not isinstance(ind_mislabelled, list):
            print("Invalid input. Please enter a valid list of numbers.")      
            
    ind_mislabelled = [int(n) for n in ind_mislabelled] 
    
    #correct the labels that were mislabelled
    for i in range(len(d['labels'])):
        if i in ind_mislabelled: 
            if d['labels'][i][0] == 0: d['labels'][i][1] = [2]*len(d['labels'][i][1])
            
            d['labels'][i][0] = ((d['labels'][i][0] + 1) % 2) #converts 0 --> 1 and 1 --> 0
            
    
    return 0


def update_tokens_label_tokens(d, tokenizer):
    '''
    This function does the portion involving making prediction on, and labelling the tokens of the job posting, 
    as part of the 'update_tokens_label' function. See the docustring of that function, for more information.
    '''
    
    #find sentences labelled '1' and whose tokens do not have a label, and call 
    # 'predict_and_label_tokens' on these sentences
    
    html_output = "black: 'O'<br>red: 'B' <br>green: 'I' <br><br>" 
    l_tok = []
    
    #will contain a list of dictionaries of the form d_tok = {'i_sent': i, 'i_l_tok': j, 'words_w_labs': []},
    #where i_sent is the index that the sentence that the tokens came from, appears in the ad, and words_w_labs
    #cooresponds to a list of lists, each list of the form [word, label_for_word], where the words are the
    #words in the sentence (not necissarily the tokens...they tokens that are seperate words have been combined 
    #into a single word)
    
    i = 0
    j = 0
    for s in d['sentences']:
        if d['labels'][i][0] == 1: #& ('na' in d['labels'][i][1]):    
            #words_and_labs = tok_sent_and_classify_toks(t_tok, t_mod, d['sentences'][i])
            
            tok_sent_obj = tokenizer(s, padding = False, truncation = False, return_tensors="pt")
            tokens = tok_sent_obj.tokens()
            
            words_and_labs = list( list(item) for item in zip(tokens, d['labels'][i][1]) )
            
            d_tok = {'i_sent': i, 'i_l_tok': j, 'words_w_labs': words_and_labs}
            l_tok.append(d_tok)
            
            html_output += "<b>" + str(j) + "</b> " + ' ' 
            html_output += html_w_labs_and_num_align_to_word([w_ll[0] for w_ll in words_and_labs],
                                                             [w_ll[1] for w_ll in words_and_labs]) 
            html_output += '<br><br>'            
            
            j += 1
        i += 1
    
    if len(l_tok) == 0:
        return 0
    
    with open("tokens_w_current_labels.html", "w", encoding="utf-8") as file:
        file.write(html_output)
    
    
    fr_user = input("Please open the file 'tokens_w_current_labels.html' and then input a list "
                                       "of the words that are mislabelled.\nThe list should be a list of "
                                    "of lists, with each sub list of the form [index_sentence, index_word, label].\n"
                                    "\t'index_sentence' is the index of the sentence of the mislabelled word,\n\t'index_word' "
                                    "is the index of the mislabelled word within the sentence, and \n\t'label' is either 0, 1 "
                                    "or 2, where \n\t\t0 <--> B <--> 'the beginning of a labelled entity', \n\t\t1 <--> I <--> "
                                    "'a word that is within in a string of words that makes up a labelled entity', and "
                                    "\n\t\t2 <--> O <--> 'the word should not be labelled'.\n" )   
    
    try:
        # Safely evaluate the input string as a Python expression to get the list
        mislab_words = ast.literal_eval(fr_user)    

    except (ValueError, SyntaxError):
        print("Invalid input. Please enter a tuple with an integer and a list.")
    
    #change the labels of the mislabelled words, as indicated by 'mislab_words', to the correct labels    
    for lst in mislab_words:
        l_tok[lst[0]]['words_w_labs'][lst[1]][1] = lst[2]

    #mapping 'labels on words' to 'labels on tokens' and put the labels in the dictionary
    for d_sent_tok in l_tok:
        sent_ind_in_d = d_sent_tok['i_sent'] 
        
        s = d['sentences'][sent_ind_in_d]
                
        for token_index in range(len(d_sent_tok['words_w_labs'])):
            d['labels'][sent_ind_in_d][1][token_index] = d_sent_tok['words_w_labs'][token_index][1]
                
    return 0   
