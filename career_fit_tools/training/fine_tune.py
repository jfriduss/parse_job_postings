# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:19:01 2023

@author: jonat_od7omk3
"""
import torch
from torch.utils.data import DataLoader

from transformers import AdamW, get_scheduler, AutoTokenizer, DataCollatorWithPadding
from transformers import TrainingArguments, AutoModelForTokenClassification
from transformers import Trainer, DataCollatorForTokenClassification

from datasets import Dataset, load_metric

from .ft_sentence_classification_helpers import gather_labelled_sentences, tokenize, CustomModel
from .ft_sentence_classification_helpers import train_custom_model

from .ft_token_classification_helpers import create_token_classification_train_test_dataset

import evaluate

import numpy as np

import os

#from data_retrieval import open_json_safe

from collections import Counter

hf_token = os.environ.get('HF_hub_token')

def fine_tune(data, sent_classifier_mod, sent_classifier_tok, tok_classifier_mod, tok_classifier_tok):

    frequency_labels_occur(data)
    
    while True:
        try:
            user_input = int(input("Choose whether to fine tune the...\n\tsentence classification model (0)\n\t"
                "the token classification model (1)\n\tboth models (2)\n\tdecide not to fine tune (3)\n"))
                                   
            if user_input in (0, 1, 2, 3):
                break
            else:
                print("Invalid input. Please enter 0, 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if user_input == 0:
        ft_sentence_classification_model(data, sent_classifier_mod, sent_classifier_tok)
    elif user_input == 1:
        ft_token_classification_model(data, tok_classifier_mod, tok_classifier_tok)
    elif user_input == 2:
        ft_sentence_classification_model(data, sent_classifier_mod, sent_classifier_tok)  
        ft_token_classification_model(data, tok_classifier_mod, tok_classifier_tok)
    else: print("The program is quitting.")
        
        
def ft_sentence_classification_model(list_of_dicts, 
                                     sent_classifier_mod, 
                                     sent_classifier_tok,
                                     num_epochs = 3, 
                                     checkpoint = "has-abi/distilBERT-finetuned-resumes-sections", 
                                     metric_name = 'f1',
                                     metric_avg_name = 'micro'):
    
    sentances_w_labels = gather_labelled_sentences(list_of_dicts)
    
    dataset = Dataset.from_dict(sentances_w_labels)
    
    #creates a DatasetDict with two keys, 'train' and 'test', each of which are Dataset's
    #with two features, 'sentences' and 'labels'
    train_test = dataset.train_test_split(test_size=0.2)
        
    tokenizer = sent_classifier_tok
    
    #creates a DatasetDict with two keys, 'train' and 'test', each of which are Dataset's
    #with four features, 'sentences', 'labels', 'input_ids', 'attention_mask'  
    
    tokenized_dataset = train_test.map(lambda batch: tokenize(batch, tokenizer), batched=True)
        
    tokenized_dataset.set_format("torch",columns=["input_ids", "attention_mask", "labels"])
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    #for now, because re fine tuning each time aquire more data, instead of working from partially fine tuned mode
    #just upload the model this way. In the future, if work from a partially fine tuned model, will need to upload 
    #the HF model from a newer checkpoint, and have a line after this, overwriting the torch linear layer with the 
    #learned weights
    
    model = sent_classifier_mod
    
    train_dataloader = DataLoader(
        tokenized_dataset["train"], shuffle=True, batch_size=32, collate_fn=data_collator)

    eval_dataloader = DataLoader(
        tokenized_dataset["test"], batch_size=32, collate_fn=data_collator)
    
   
    optimizer = AdamW(model.parameters(), lr=5e-5)

    num_training_steps = num_epochs * len(train_dataloader)
    
    lr_scheduler = get_scheduler(
        "linear",
        optimizer=optimizer,
        num_warmup_steps=0,
        num_training_steps=num_training_steps)

    metric = load_metric(metric_name)
    

    
    train_custom_model(model, device, num_epochs, num_training_steps, train_dataloader, eval_dataloader,
                      optimizer, lr_scheduler, metric, metric_avg_name)   


def ft_token_classification_model(list_of_dicts, 
                                  tok_classifier_mod, 
                                  tok_classifier_tok,
                                  metric = "seqeval"):
    
    model = tok_classifier_mod
    tokenizer = tok_classifier_tok    
    
    #creates a DatasetDict with two keys, 'train' and 'test', each of which are Dataset's
    #with four features, 'input_ids', 'token_type_ids', 'attention_mask', and'labels'
    train_test = create_token_classification_train_test_dataset(list_of_dicts, tokenizer)
    
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    
    args = TrainingArguments(
        output_dir = 'tok_train_info', 
        overwrite_output_dir = 'True',
        evaluation_strategy = "epoch",
        save_strategy = "epoch",
        learning_rate = 2e-5,
        num_train_epochs = 3,
        weight_decay = 0.01,
        push_to_hub = True,
        hub_token = hf_token )    
    
    trainer = Trainer(
        model = model,
        args = args,
        train_dataset = train_test["train"],
        eval_dataset = train_test["test"],
        data_collator = data_collator,
        compute_metrics = compute_metrics,
        tokenizer = tokenizer)

    trainer.train()
    trainer.save_model('tok_train_info')    


def compute_metrics(eval_preds):
    logits, labels = eval_preds
    
    #note: how the logits are processed depends on the head of the model 
    predictions = np.argmax(logits[0], axis=-1) 
    label_names = {0: 'B', 1: 'I', 2: 'O'}
    
    # Remove ignored index (special tokens) and convert to labels
    true_labels = [[label_names[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [label_names[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    
    metric = evaluate.load("seqeval")
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }
    


def frequency_labels_occur(list_of_dicts):
    '''
    Takes the list of dicts, and prints the number of sentences labelled with each respective label
    '''
    
    all_labels_sentence_classification = []
    all_labels_token_classification = []
    
    for d in list_of_dicts:
        for i in range(len(d['labels'])):
            all_labels_sentence_classification.append(d['labels'][i][0])
            all_labels_token_classification.extend(d['labels'][i][1])
        
    element_count_sc = Counter(all_labels_sentence_classification)
    top_3_elements_sc = element_count_sc.most_common(3)

    element_count_tc = Counter(all_labels_token_classification)
    top_4_elements_tc = element_count_tc.most_common(4)    
        
    print("The breakdown of the sentence classification data is:\t")
    print_label_percentages(top_3_elements_sc)
    print("\nThe breakdown of the token classification data is:\t")
    print_label_percentages(top_4_elements_tc)
    
    return 0


def print_label_percentages(data_list):
    total_data = sum(count for label, count in data_list if label != 'na')
    
    for label, count in data_list:
        if label != 'na':
            percentage = (count / total_data) * 100
            print(f"Label '{label}': {count} data points ({percentage:.2f}% of total)")