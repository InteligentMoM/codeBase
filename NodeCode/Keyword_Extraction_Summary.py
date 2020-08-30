#!/usr/bin/env python
# coding: utf-8

# In[12]:


from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import argparse
import pandas as pd


# In[7]:


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_text_file_path", required=True, help="Please Enter Text file path for keyword highlight...")
ap.add_argument("-o", "--output_text_file_path", required=True, help="Please Enter Text file path for keyword highlight...")
args = vars(ap.parse_args())


# In[2]:


nlp = spacy.load('en_core_web_sm')

class TextRank4Keyword():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    
    def set_stopwords(self, stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """Print top number keywords"""
        res_words=[]
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            #print(key + ' - ' + str(value))
            res_words.append(key)
            if i > number:
                break
        return res_words
        
    def analyze(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""
        
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Pare text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight


# In[3]:


def get_keyTags(text):
    res=''
    #text = '''
    #January Series is one of the challenging one, but the motivation after the previous huge series is still at the highest possible level. 
    #'''
    tr4w = TextRank4Keyword()
    #tr4w.analyze(text, candidate_pos = ['NOUN','ADJ','VERB'], window_size=4, lower=False)
    tr4w.analyze(text, candidate_pos = ['NOUN','PROPN','ADJ','NUM','VERB'], window_size=4, lower=False)
    res=tr4w.get_keywords(5)
    res=[items for items in res if len(items)> 1]
    from itertools import combinations 
    def rSubset(arr, r): 
        return set(combinations(arr, r))
    comb =rSubset(res,2)
    remove=[]
    dual_res=[]
    for item in comb:
        if item[0].isalpha() and item[1].isalpha():
            if (len (re.findall(' '.join(item), text)) ) >=1:
                dual_res.append(' '.join(item))
                remove.extend([item[0],item[1]])
            elif (len (re.findall(' '.join(item[::-1]), text)) ) >=1:
                dual_res.append(' '.join(item[::-1]))
                remove.extend([item[0],item[1]])

    single_res = res.copy()
    for elem in res:
        if elem in remove:
            single_res.remove(elem)

    singular_res = []
    for item in single_res:
        singular_res.append(item)
    return singular_res


# In[ ]:


with open(args['input_text_file_path'], 'r') as file:
    text = file.read().replace('\n', '')


# In[23]:


import re
#text ="""'Eating Raoul, so first of all, thanks a lot for trying out this and let us see what is that we have achieved using the Watson Workflow. Can you explain me what you have attempted here?', ''"""
def highlight(text):
    res=get_keyTags(text)
    new_text=[]
    for texts in text.split():
        if texts in res:
            texts='<mark>'+texts+'</mark>'
            new_text.append(texts)
        else:
            new_text.append(texts)
    highlighted_text=' '.join(new_text)
    return highlighted_text


# In[11]:


highlighted_text = highlight(text)
print(highlighted_text)


# In[63]:


text_file = open(args['output_text_file_path'], "w")
n = text_file.write(highlighted_text)
text_file.close()


# In[ ]:




