#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse


# In[1]:


from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig


# In[ ]:


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--audio_name", required=True, help="Please Enter Audio File Name(Without extension)")
args = vars(ap.parse_args())


# In[2]:


speech_config = SpeechConfig(subscription="__KEY", region="Region")


# In[3]:


audio_config = AudioOutputConfig(filename="public/python/output_audio_files/"+args['audio_name']+"_summary.wav")


# In[4]:


with open("summary/"+args['audio_name']+"_summary.txt", 'r') as file:
    data = file.read().replace('\n', '')


# In[5]:


data


# In[11]:


synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
synthesizer.speak_text_async(data)


# In[ ]:




