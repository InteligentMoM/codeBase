#!/usr/bin/env python
# coding: utf-8

# In[22]:


import torch
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import argparse
import pandas as pd


# In[23]:


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--audio_name", required=True, help="Please Enter Audio File Name(Without extension)")
args = vars(ap.parse_args())


# In[24]:


file_name = "transcripts/"+args['audio_name']+"_transcript.csv"
#file_name ="transcripts/test_transcript.csv"


# In[25]:


dataset = pd.read_csv(file_name)


# In[26]:


dataset.head()


# In[27]:


model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')


# In[28]:


text=[]
for index,rows in dataset.iterrows():
  text.append(dataset['Transcript'][index])

text = str(text)


# In[29]:



preprocess_text = text.strip().replace("\n","")
t5_prepared_Text = "summarize: "+preprocess_text
print ("original text preprocessed: \n", preprocess_text)

tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


# summmarize
summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=100,
                                    early_stopping=True)

output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)


# In[31]:


print(output)


# In[30]:


type(output)


# In[ ]:


text_file = open("summary/"+args['audio_name']+"_summary.txt", "w")
n = text_file.write(output)
text_file.close()
