#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import argparse
import os
from subprocess import call
from os import path
from pydub import AudioSegment


# In[ ]:


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--audio_name", required=True, help="Please Enter Audio File Name...")
args = vars(ap.parse_args())


# In[ ]:


file = args["audio_name"]


# In[2]:


#file = 'wavs/test.wav'


# In[3]:


f = file.split(".")
file_format = f[1]
rest = f[0]


# In[4]:


file_format


# In[5]:


f1 = rest.split("/")
file_name = f1[-1]
file_name


# In[6]:


# files                                                                         
src = "wavs\\"+file_name+"."+file_format
dst = "wavs\\"+file_name+".wav"
print(src)
print(dst)

import os
    
print(os.getcwd())


if file_format != "wav":
    # sound = AudioSegment.from_mp3(src)
    # sound.export(dst, format="wav")
    import subprocess 
    subprocess.call(['ffmpeg', '-i', src, dst])
    print("Converted")
else:
    print("Already in WAV Format")


# In[ ]:


## Executing python scripts now


# In[16]:


a = []


# In[17]:


cmd = "python Enter_Audio_Name.py --audio "+dst
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[18]:


if os.system('python speakerDiarization.py')==0:
    a.append("Yes")
else:
    a.append("No")


# In[20]:


cmd = "python Audio_Segment.py --audio_name "+file_name
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[22]:


cmd = "python Azure_Speech2Text_Transcription.py --audio_name "+file_name
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[24]:


cmd = "python Keyword_Extraction_Transcript.py --input_text_file_path transcripts/"+file_name+"_transcript.csv --output_text_file_path transcripts/"+file_name+"transcript_with_keyword.csv"
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[25]:


cmd = "python Summarization.py --audio_name "+file_name
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[27]:


cmd = "python Keyword_Extraction_Summary.py --input_text_file_path summary/"+file_name+"_summary.txt --output_text_file_path summary/"+file_name+"_summary_extracted_keyword.txt"
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[28]:


cmd = "python TextToSpeech.py --audio_name "+file_name
if os.system(cmd)==0:
    a.append("Yes")
else:
    a.append("No")


# In[46]:


data = pd.read_csv("transcripts/"+file_name+"transcript_with_keyword.csv")
data.to_json("transcripts/"+file_name+"transcript_with_keyword.json", orient="records")


# In[33]:


if os.path.exists(dst):
    a.append("Yes")
else:
    a.append("No")


# In[34]:


if os.path.exists("Speaker_Timestamp.csv"):
    a.append("Yes")
else:
    a.append("No")


# In[36]:


if os.path.exists("Speaker_time.csv"):
    a.append("Yes")
else:
    a.append("No")


# In[37]:


if os.path.exists("Audio_File_Name.csv"):
    a.append("Yes")
else:
    a.append("No")


# In[38]:


if os.path.exists("transcripts/"+file_name+"_transcript.csv"):
    a.append("Yes")
else:
    a.append("No")


# In[39]:


if os.path.exists("transcripts/"+file_name+"transcript_with_keyword.csv"):
    a.append("Yes")
else:
    a.append("No")


# In[40]:


if os.path.exists("summary/"+file_name+"_summary.txt"):
    a.append("Yes")
else:
    a.append("No")


# In[41]:


if os.path.exists("summary/"+file_name+"_summary_extracted_keyword.txt"):
    a.append("Yes")
else:
    a.append("No")


# In[42]:


if os.path.exists("public/python/output_audio_files/"+file_name+"_summary.wav"):
    a.append("Yes")
else:
    a.append("No")


# In[47]:


if os.path.exists("transcripts/"+file_name+"transcript_with_keyword.json"):
    a.append("Yes")
else:
    a.append("No")


# In[48]:





# In[49]:


if "No" in a:
    print("Error Occured")
else:
    print("All Good")


# In[ ]:




