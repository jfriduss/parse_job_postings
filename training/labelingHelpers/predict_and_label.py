# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 12:03:53 2023

@author: jonat_od7omk3
"""
import ast


from .predict_and_label_helpers import classify_sentences, tok_sent_and_classify_toks
from .predict_and_label_helpers import html_w_labs_and_num_align_to_word

#if want to have the function have default models and tokenizers, uncomment the below
#(though it is probably a bad idea)

# from transformers import AutoModelForTokenClassification, AutoTokenizer
#from training.ft_sentence_classification_helpers import CustomModel

# default_sent_classifier_mod = CustomModel("has-abi/distilBERT-finetuned-resumes-sections", num_labels = 2)
# default_sent_classifier_tok = AutoTokenizer.from_pretrained("has-abi/distilBERT-finetuned-resumes-sections")
# default_tok_classifier_mod = AutoModelForTokenClassification.from_pretrained("jjzha/jobbert_knowledge_extraction")
# default_tok_classifier_tok = AutoTokenizer.from_pretrained("jjzha/jobbert_knowledge_extraction")



def predict_and_label(d, sent_classifier_mod, sent_classifier_tok, tok_classifier_mod, tok_classifier_tok):

                      # sent_classifier_mod = default_sent_classifier_mod, 
                      # sent_classifier_tok = default_sent_classifier_tok, 
                      # tok_classifier_mod = default_tok_classifier_mod, 
                      # tok_classifier_tok = default_tok_classifier_tok):
    '''
    This function takes a dictionary with information about the job description, in the same form used throughout the project:
        -keys: 'job_id', 'sentences', 'helpers', 'labels', where labels has both the sentence classification and NER labels
        
    It then does the following with this dictionary:
        - has the sentence classification model predict whether or not the not-already-classified sentences have relavent tokens
        - outputs the sentences the model attempted to label (bolded if model predicts has relavent tokens/normal if not) for 
            human annotator to check
        - the human annotator indicates which predictions aren't correct
        - the sentences labels are updated accordingly
        
        Next it does the same thing for token classification:
            - has the token classification model predict how each token should be classified (for tokens in sentences that are
                labelled "has tokens that should be annotated" and are not already labelled)
            - outputs the tokens the model attempted to label (colored accordingly to label) for human annotator to check
            - the human annotator inidicates which predictions aren't correct
            - the token labels are updated accordingly        
    '''
    
    #does the aspect of process described above, that pertains to creating labels for sentence classification
    predict_and_label_sentences(d, sent_classifier_mod, sent_classifier_tok)
    
    #does the aspect of process described above, that pertains to creating labels for NER
    predict_and_label_tokens(d, tok_classifier_mod, tok_classifier_tok)
    

def predict_and_label_sentences(d, s_mod, s_tok):
    '''
    This function does the portion involving making prediction on, and labelling the sentences of the job posting, 
    as part of the 'predict_and_label' function. See the docustring of that function, for more information.
    '''
    
    #find sentences without a label, and put them in a dictionary that has
    #a list of indices that each sentence cooresponds to, the sentence itself
    #and eventually will have the predicted label, too. This is necessary,
    #because what if some sentences have already been labelled by the autolabeller.

    d_sent = {'indices': [], 'sents': [], 'labs': []}
    
    i = 0
    for s in d['sentences']:
        if d['labels'][i][0] == 'na':
            d_sent['sents'].append(d['sentences'][i])
            d_sent['indices'].append(i)
        i += 1
        
    if len(d_sent['sents']) == 0:
        return 0

    #have sentence classification model make predictions on the sentences without labels     
    pred_sentence_labels = classify_sentences(s_tok, s_mod, d_sent['sents'])
    d_sent['labs'].extend(pred_sentence_labels)
    
    #write sentences, and the index in the d['sents'] that they appear, to an html file
    #with sentences bolded if model predicts has relavent tokens and normal if not
    
    html_sentences_and_indices = "Black: 'Does not contain words to label'\nRed: 'contains words to label'<br><br>"
    for i in range(len(d_sent['sents'])):
        html_sentences_and_indices += "<b>" + str(i) + "</b> "
        if (d_sent['labs'][i] == 0): html_sentences_and_indices += d_sent['sents'][i]
        if (d_sent['labs'][i] == 1): html_sentences_and_indices += "<span style=\"color: red;\">" + d_sent['sents'][i] + "</span>"
        html_sentences_and_indices += '<br>'
        
    with open("predictions_on_sentences.html", "w", encoding='utf-8') as file:
        file.write(html_sentences_and_indices)     
        
    #asks human annotator to indicate which sentences were labelled incorrectly
    ind_mislabelled = input("Please open the file 'predictions_on_sentences.html' and then input a list "
                                 "with the indices of the sentences that were labelled incorrectly.")

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
    for i in range(len(d_sent['labs'])):
        if i in ind_mislabelled: d_sent['labs'][i] = ((d_sent['labs'][i] + 1) % 2) #converts 0 --> 1 and 1 --> 0    
    
    #put labels into the dictionary
    i = 0
    for index in d_sent['indices']:
        d['labels'][index][0] = d_sent['labs'][i]
        i += 1
    
    return 0


def predict_and_label_tokens(d, t_mod, t_tok):
    '''
    This function does the portion involving making prediction on, and labelling the tokens of the job posting, 
    as part of the 'predict_and_label' function. See the docustring of that function, for more information.
    '''
    
    #find sentences labelled '1' and whose tokens do not have a label, and call 
    # 'predict_and_label_tokens' on these sentences
    
    html_output = "black: 'O'\nred: 'B' \ngreen: 'I' <br><br>" 
    l_tok = []
    
    #will contain a list of dictionaries of the form d_tok = {'i_sent': i, 'i_l_tok': j, 'words_w_labs': []},
    #where i_sent is the index that the sentence that the tokens came from, appears in the ad, and words_w_labs
    #cooresponds to a list of lists, each list of the form [word, label_for_word], where the words are the
    #words in the sentence (not necissarily the tokens...they tokens that are seperate words have been combined 
    #into a single word)
    
    i = 0
    j = 0
    for s in d['sentences']:
        if d['labels'][i][0] == 1 & ('na' in d['labels'][i][1]):    
            words_and_labs = tok_sent_and_classify_toks(t_tok, t_mod, d['sentences'][i])
            
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
    
    with open("predictions_on_tokens.html", "w", encoding="utf-8") as file:
        file.write(html_output)
    
    
    fr_user = input("Please open the file 'predictions_on_tokens.html' and then input a list "
                                       "of the words that were mislabelled.\nThe list should be a list of "
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
        sent_enc = t_tok(s, padding = False, truncation = False, return_tensors="pt")
        word_ids = sent_enc.word_ids()
        
        token_index = 0
        label_index = 0
        
        w_id_prev = -1
        
#         print(d_sent_tok['words_w_labs'])
#         print(word_ids)
#         print('\n')
        for w_id in word_ids: #continue here, making sure this part works as expected
#             print(label_index)
            if w_id == None: d['labels'][sent_ind_in_d][1][token_index] = -100
            
            elif ( (w_id == w_id_prev) | (w_id_prev == None) ):
                d['labels'][sent_ind_in_d][1][token_index] = d_sent_tok['words_w_labs'][label_index][1]
                
            else:
                label_index += 1
                d['labels'][sent_ind_in_d][1][token_index] = d_sent_tok['words_w_labs'][label_index][1]
            
            w_id_prev = w_id
                
            token_index += 1
        
    return 0        
        

