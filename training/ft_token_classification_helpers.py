# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:26:00 2023

@author: jonat_od7omk3
"""
from datasets import Dataset

def create_token_classification_train_test_dataset(list_of_dicts, tokenizer):
    
    d_tok_class =  {'input_ids': [], 'token_type_ids': [], 
                    'attention_mask': [], 'labels':[]}

    for i in range(len(list_of_dicts)):
        d = list_of_dicts[i]
        inds_w_toks = [j for j in range(len(d['labels'])) if d['labels'][j][0] == 1] 
        #need to check whether or not the tokens in the sentence have been labelled yet!
        
        for k in inds_w_toks:
            if 'na' not in d['labels'][k][1]: 
                tok_outp = tokenizer(d['sentences'][k])

                d_tok_class['input_ids'].append(tok_outp['input_ids'])
                d_tok_class['token_type_ids'].append(tok_outp['token_type_ids'])
                d_tok_class['attention_mask'].append(tok_outp['attention_mask'])
                d_tok_class['labels'].append(d['labels'][k][1])
 
    
    dataset_tok_class = Dataset.from_dict(d_tok_class)
    train_test = dataset_tok_class.train_test_split(test_size=0.2)
    
    return train_test