# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:26:00 2023

@author: jonat_od7omk3
"""
import os

import torch
import torch.nn as nn

from transformers import AutoModel, AutoConfig
from transformers.modeling_outputs import TokenClassifierOutput
from tqdm.auto import tqdm


def gather_labelled_sentences(list_of_dicts):
    d_sent = {'sentences': [], 'labels': [] }

    for d in list_of_dicts:
        for i in range(len(d['sentences'])):
            if (d['sentences'][i] not in d_sent['sentences']) and (d['labels'][i][0] != 'na' ) :
                d_sent['sentences'].append(d['sentences'][i])
                d_sent['labels'].append(d['labels'][i][0])    
                
    return d_sent


def tokenize(batch, tokenizer): 
      return tokenizer(batch["sentences"], truncation=True,max_length=512)
        
    
class CustomModel(nn.Module):
    def __init__(self,checkpoint,num_labels):
        super(CustomModel,self).__init__()
        self.num_labels = num_labels

        #Load Model with given checkpoint and extract its body
        self.model = AutoModel.from_pretrained(checkpoint,config=AutoConfig.from_pretrained(checkpoint, output_attentions=True,output_hidden_states=True))
        self.model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(768, num_labels).to(self.model.device) # load and initialize weights

    def forward(self, input_ids=None, attention_mask=None,labels=None):
        #Extract outputs from the body
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)

        #Add custom layers
        sequence_output = self.dropout(outputs[0]) #outputs[0]=last hidden state

        logits = self.classifier(sequence_output[:,0,:].view(-1,768)) # calculate losses

        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

        return TokenClassifierOutput(loss=loss, logits=logits, hidden_states=outputs.hidden_states,attentions=outputs.attentions)    
        
    def save_hybrid_hf_torch_model(self, torch_f_name): #likely need names that want to save the HF stuff under, too
      '''
      This method was created so that models could be trained with gpu acceleration on a google colab, and then used to
      make predictions locally with a jupyter notebook. It takes a file name (without the .pth) to name the state dictionary
      that has the contents of the pytorch linear layer, and then creates a folder "model_contents" that has the state dictionary,
      as well as a folder, "hf", which contains the config.json and pytorch_model.bin files, required to rebuild the hugging face
      portions of the model
      '''
    
      on_colab = input('Is this being run in a google colab? (y/n)')
    
      if (on_colab == 'y'):
        print("Storing the constitutents of the model required to rebuild it in the folder 'model_contents' in your Google Drive.")
        #the below code assumes that you have imported drive from google.colab and
        #then run "drive.mount('/content/drive')"
    
        folder_path = '/content/drive/MyDrive/model_contents'
    
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
        torch.save(self.classifier.state_dict(), folder_path + '/' + torch_f_name + '.pth' )
        self.model.save_pretrained(folder_path + '/hf') #note: the pytorch_model.bin is a state dictionary as well
    
      if (on_colab == 'n'):
        print('write this part of the function if I actually ever need to use it outside of a colab!')    
        

    def overwrite_w_trained_weights(self, path2model_info, f_name_lin):
        '''
        This method is used to rebuild the model, given the files that the method 'save_hybrid_hf_torch_model' output
        '''
        
        self.model = self.model.from_pretrained(path2model_info)
        #note: the below, in place, overwrites the contents of self.classifier with weights from google colab 
        if torch.cuda.is_available():
            self.classifier.load_state_dict(torch.load(f_name_lin, map_location=torch.device('cuda')))
        else:
            self.classifier.load_state_dict(torch.load(f_name_lin, map_location=torch.device('cpu')))  
            

def train_custom_model(custom_model, device, num_epochs, num_training_steps, train_dataloader, eval_dataloader,
                      optimizer, lr_scheduler, metric, metric_avg_name):

    progress_bar_train = tqdm(range(num_training_steps))
    progress_bar_eval = tqdm(range(num_epochs * len(eval_dataloader)))


    for epoch in range(num_epochs):
        custom_model.train()
        for batch in train_dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = custom_model(**batch)
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            progress_bar_train.update(1)

        custom_model.eval()
        for batch in eval_dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.no_grad():
                outputs = custom_model(**batch)

            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)
            metric.add_batch(predictions=predictions, references=batch["labels"])
            progress_bar_eval.update(1)

        print(metric.compute(average = metric_avg_name)) #need to set the 'average' here, if a multiclassification problem            