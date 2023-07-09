import pandas as pd
import numpy as np
import time
import re
import nltk
from nltk import sent_tokenize, word_tokenize

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Split job descr into sentences
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
def sentece_preprocessing(inputjd):
    ## NOTE: sent_tokenize requires a punctuation like '.' to split sentences
    inputjd = inputjd.lower()
    
    # Handle first new lines, then whitespaces
    inputjd = re.sub(r"\r?\n", ". ", inputjd) # Replace new lines with dot
    inputjd = re.sub(r"\s{2,}", " ", inputjd) # Replace too many spaces with one space (this will also treat \n)
    # Clean repeated !?.
    inputjd = re.sub(r"!{2,}", "!", inputjd)
    inputjd = re.sub(r"\?{2,}", "?", inputjd)
    inputjd = re.sub(r" +\.+", ".", inputjd)
    inputjd = re.sub(r"\.+", ".", inputjd)
    # URLs or emails
    inputjd = re.sub(r"https://[^ ]+", "", inputjd)
    inputjd = re.sub(r"www\.[^ ]+", "", inputjd)
    inputjd = re.sub(r"[^ ]+@[^ ]+.", "", inputjd)
    # Split
    inputjd = sent_tokenize(inputjd)
    # Clean super short sentences below n word-tokens | There're bullet points with just 2 words like 'Python experience', so be careful
    min_n=2; max_n=384
    final = [s for s in inputjd if len(word_tokenize(s)) >= min_n]
    long_sent = [s for s in inputjd if len(word_tokenize(s)) > max_n]
    if len(long_sent) > 0:
        print(long_sent)
    return final

Job_Info['Pre processed sentences'] = Job_Info['Job Description'].apply(sentece_preprocessing) # split into sentences
print(len(Job_Info))

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Bring sentences to the rows, together with the job id
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
def sentence_row(df_):
    IDs_ = []; sents_ = []; embeddings_ = []; i = 0; i_last = 0
    for idx, row in df_.iterrows():
        for sen in list(row['Pre processed sentences']):
            IDs_.append(row['Job ID'])
            sents_.append(sen)
    df_sentences = pd.DataFrame({'Job ID':IDs_, 'Sentence':sents_})
    return df_sentences

Job_Sentences = sentence_row(Job_Info)
print(len(Job_Sentences))

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
# Generate sentence embeddings
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
from sentence_transformers import SentenceTransformer # Will save data to: /Users/name/.cache/huggingface/hub

# Donwnload sBERT model from huggingface
model_name = 'sentence-transformers/all-mpnet-base-v2'
model = SentenceTransformer(model_name)
print(model)

def embed_save(df_, model_):
    embedding_dim_ = 768; embeddings_ = []; i = 0; i_last = 0
    st_ = time.time()
    print("-------- Start")
    for idx, row in df_.iterrows():
        embd_ = model.encode(row['Sentence']) # Create embeddings
        embeddings_.append(embd_)
        if i - i_last == 250:
            elapsed_ = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-st_))
            i_last = i
            print(":: {} Sentences embedded in: {}".format(i, elapsed_))
        i += 1
    
    # Save into df
    col_ids = list(range(0, embedding_dim_))
    col_names = ['emb_d_'+str(col_ids[i]) for i in range(embedding_dim_)] # create col names

    embeddings_arr = np.array(embeddings_) # convert to np array
    for i in range(len(col_names)):
        df_[col_names[i]] = embeddings_arr[:, i]
    
    return df_

# Generate embeddings
df_embeddings = embed_save(Job_Sentences, model)

# Save to file
df_embeddings.to_csv(_Path+'/sentences_embeddings.csv', header=True, index=False, sep='|', mode='w')
print(df_embeddings.shape)
