# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 12:15:23 2023

@author: jonat_od7omk3
"""

import torch


def classify_sentences(tokenizer, model, sentences):
    '''
    takes a CustomModel, the tokenizer that goes with the model, and a list of sentences, 
    and returns the list of predicted labels that coorespond to each sentence
    
    note: changed this from trying to create a batch of all of the sentences, and then processing all at once,
    to running the model on each sentence one at a time. Sped up the classification by 20-100 times, and stopped 
    the memory errors from occuring every few runs. 
    '''
    
    labels_w_max_prob = []
    for s in sentences:
        tokenized_sentence = tokenizer(s)
        
        #tokenizer outputs lists, we need tensors
        tokenized_sentence['input_ids_tens'] = torch.Tensor([tokenized_sentence['input_ids']])
        tokenized_sentence['attention_mask_tens'] = torch.Tensor([tokenized_sentence['attention_mask']])
        
        #has issues unless the data in the tensors are stored as int64's
        tokenized_sentence['input_ids_tens'] = tokenized_sentence['input_ids_tens'].to(torch.int64)
        tokenized_sentence['attention_mask_tens'] = tokenized_sentence['attention_mask_tens'].to(torch.int64)
        
        outp = model.forward(input_ids=tokenized_sentence['input_ids_tens'],
                             attention_mask=tokenized_sentence['attention_mask_tens'])
        
        outp_probabilities = torch.nn.functional.softmax(outp.logits, dim=-1)
        lab_w_max_prob = torch.argmax(outp_probabilities, dim=1) #find the index that the max probability appears, in each row
        labels_w_max_prob.extend(lab_w_max_prob.tolist())
        
    return labels_w_max_prob


def tok_sent_and_classify_toks(tokenizer, model, sentence):
    '''
    takes a model, the tokenizer that goes with the model, and a sentence from a job ad, 
    and then outputs the sentence, color coded according to how the model labels the sentence

    note: right now, the 'attention_mask' and 'token_type_ids' that the tokenizer is outputting are not being used, which will
    likely be an issue in some cases. Figure this out!

    reminder: when doing NER, one way of labelling is 'BIO' tagging:
        B - beginning of the phrase
        I - interior of the phrase
        O - everything else
        
    example: Corn(O) grows(O) in(O) the(O) United(B_Country) States(I_Country) of(I_Country) America(I_Country)
    
    the t_pred is vector with 3 dimensions, each of whose value cooresponds to the probability that the token should be assigned
    that label. To get what index cooresponds to what label, use model.config.id2label
    
    basic process: 
        -tokenize the sentence
        - make it its own batch, because the model expects multiple sentences, not a single one
        - get an output for each token, convert those to probabilities of labels, via softmax
        - do a processing sequence to convert these to predictions on the words of a sentence:
            - make a list of tuples, where each tuple has (token, word_id, prediction)
                - word_id tells you whether the token/prediction cooresponds to something the model put int (e.g. a [SEP]),
                a subword, or an entire word. E.g. tokens = [..., 's', '##cal', '##ing', ...], word_id = [..., 14, 14, 14, ...].
                If I forget what the significance of word_ids are, print tokenizer(sentence).token() next to 
                tokenizer(sentence).word_ids(), next to the predictions, to understand. Basically, the word_ids tell you how
                to merge the tokens together to form words, and which tokens are created by the model, and not a part of the 
                input sentence
            - remove the tuples that coorespond to tokens the model created (e.g. [SEP] and [CLS]). Know which these are, because
            their word_id is None
            - group the tuples into sublists, according to whether their word_ids are the same/they are sub parts of the same 
            word (using the 'group_tuples_by_first_index' function)
            - concatenate the subwords and assign labels to them, by taking a weighted average of the predictions on each part
            of the subword (using the 'process_and_predict' function). This outputs a list of tuples whose first index is a 
            word (e.g. the tokens that are part of subwords are now combined) and the second index, the label for that word
        - combine the words into a sentence, color coded according to the label that was assigned to them
    '''    
    
    t_sent_enc = tokenizer(sentence, padding = False, truncation = False, return_tensors="pt")
    
    #need to convert the tensor to a list, put that list into a list, then convert that to a batch of a single tensor, and 
    #then put it into the model, to get the model to work on it

    t_for_model =  torch.tensor([t_sent_enc['input_ids'][0].tolist()])
    
    t_outp = model(t_for_model)
    t_pred = torch.nn.functional.softmax(t_outp.logits, dim = -1)  
    
    helper_l = list(zip(t_sent_enc.tokens(), t_sent_enc.word_ids(), t_pred.tolist()[0]))
    helper_l = [el for el in helper_l if el[1] != None]    
    
    grouped_helper_l = group_tuples_by_first_index(helper_l)
    # word_w_predictions = process_and_predict(grouped_helper_l)
    
    return process_and_predict(grouped_helper_l)


def group_tuples_by_first_index(tuples_list):
    '''
    used in the 'label_skills_in_sentence_and_print' to created sublists of tuples, each of which belong to the 
    same word. for example, 
        [ ..., 
        ('s', 14, [2.7788328225142322e-06, 2.5301173991465475e-06, 0.9999946355819702]),
        ('##cal', 14, [2.811010062941932e-06, 2.4472606128256302e-06, 0.9999947547912598]),
        ('##ing', 14, [2.5843060029728804e-06, 2.141523054888239e-06, 0.999995231628418]),
        ('to', 15, [2.951515398308402e-06, 3.0770443117944524e-06, 0.9999939203262329]),
        ..., ]
        
    becomes:
        [ ..., 
        
        [ ('s', 14, [2.7788328225142322e-06, 2.5301173991465475e-06, 0.9999946355819702]),
            ('##cal', 14, [2.811010062941932e-06, 2.4472606128256302e-06, 0.9999947547912598]),
            ('##ing', 14, [2.5843060029728804e-06, 2.141523054888239e-06, 0.999995231628418]),
            ('to', 15, [2.951515398308402e-06, 3.0770443117944524e-06, 0.9999939203262329]) ] ,
        
        [ ('to', 15, [2.951515398308402e-06, 3.0770443117944524e-06, 0.9999939203262329]) ] ,
        
        ...]
        
    the tuples cooresponding to 'scaling' all are grouped into a sublist, the tuple cooresponding to 'to' is grouped, etc.
    '''
    grouped_dict = {}
    
    for tup in tuples_list:
        key = tup[1]  # Assuming the first index is at position 1
        if key in grouped_dict:
            grouped_dict[key].append(tup)
        else:
            grouped_dict[key] = [tup]
    
    grouped_list = list(grouped_dict.values())
    return grouped_list


def process_and_predict(list_of_lists):
    '''
    used in the 'label_skills_in_sentence_and_print' to take a list of lists of tuples, that are output by 
    'group_tuples_by_first_index', and then converts these to a list of tuples, with each tuple having a word, 
    and the label assigned to that word, where the label is determined by taking a weighted average of the 
    predictions that the model outputs on the tokens that make up the word
    '''
    results = []
    
    for sublist in list_of_lists:
        concatenated_string = ''
        weighted_probabilities = [0, 0, 0]  # Initialize weighted probabilities for each label
        
        for tup in sublist:
            concatenated_string += tup[0].replace('##', '')  # Remove '##' and concatenate
            probabilities = tup[2]  # Assuming probabilities are at position 2
            weighted_probabilities = [
                wp + prob for wp, prob in zip(weighted_probabilities, probabilities)
            ]
        
        total_tuples = len(sublist)
        weighted_probabilities = [wp / total_tuples for wp in weighted_probabilities]
        
        # Make prediction based on weighted average probabilities
        prediction = weighted_probabilities.index(max(weighted_probabilities))
        
        results.append([concatenated_string, prediction])
    
    return results


def html_w_labs_and_num_align_to_word(words, labels):
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            .word {{
                display: inline-block;
                margin-right: 10px;
                text-align: center;
            }}
            .red {{
                color: red;
            }}
            .green {{
                color: green;
            }}
            .black {{
                color: black;
            }}
        </style>
    </head>
    <body>
        {}
    </body>
    </html>
    """
    
    word_html = ""
    for index, (word, label) in enumerate(zip(words, labels)):
        color_class = "black"
        if label == 0:
            color_class = "red"
        elif label == 1:
            color_class = "green"
        
        word_html += f'<div class="word {color_class}">{word}<br/>{index}</div>'
    
    final_html = html_template.format(word_html)
    return final_html