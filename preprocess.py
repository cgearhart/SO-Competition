from __future__ import division
from collections import Counter
from functools import wraps
import competition_utilities as cu
import gearley_utilities as gu
import numpy as np
import datetime as dt
import pandas as pd
import preprocess
import string
import re

def camel_to_underscores(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

##############################################################
###### INCLUSION TEST FUNCTIONS
##############################################################

def code_lines(df):
    return '\n'.join([line.lstrip() for line in df.splitlines() if line.startswith(('\t','    '))]) # does not preserve indentation

def text_lines(df):
    return '\n'.join([line for line in df.splitlines() if not line.startswith(('\t','    ')) and len(line) > 0]) # non-empty lines that aren't indented

def num_paragraphs(df):
    p_count = df["TextLines"].apply(lambda x: x.count('\n'))
    return pd.DataFrame.from_dict({"NumParagraphs": p_count})

def num_sentences(df):
    s_count = df["TextLines"].apply(count_end_marks)
    return pd.DataFrame.from_dict({"NumSentences": s_count})

def num_lines_code(df):
    l_count = df["CodeLines"].apply(lambda x: len(x.splitlines()))
    return pd.DataFrame.from_dict({"NumLinesCode": l_count})

def len_lines_code(df):
    c_len = df["CodeLines"].apply(avg_line_len)
    return pd.DataFrame.from_dict({"LenLinesCode": c_len})

def len_sentences(df):
    s_len = df["TextLines"].apply(avg_sentence_len)
    return pd.DataFrame.from_dict({"LenSentences": s_len})

def time_to_close(df):
    

##############################################################
###### PROCESSING FUNCTIONS
##############################################################

def count_end_marks(text):
    return sum([text.count(sym) for sym in ['.','!','?']])

def avg_line_len(code):
    len_lines = [len(line) for line in code]
    return 0 if len(len_lines) == 0 else sum(len_lines)/len(len_lines)

def avg_sentence_len(text):
    text = text.translate(string.maketrans('!?','..'))
    text = text.split('.')
    sent_lens = [len(sent.lstrip()) for sent in text]
    return 0 if len(sent_lens) == 0 else sum(sent_lens)/len(sent_lens)

###########################################################

def process_and_pickle(function_list,data,dataFileName="default"):
    fea_df = pd.DataFrame(index=data.index) # creates a dataframe object with rows matched to "data"
    for name in function_list:
        if name in data:
            fea_df = fea_df.join(data[name])
        else:
            try:
                fea_df = fea_df.join(gu.get_dataframe(name+dataFileName))
            except IOError:
                print 'No dataframe pickle named {} found.'.format(name)
                
                new_df = getattr(preprocess,
                                 camel_to_underscores(name))(data)
                
                
                fea_df = fea_df.join(getattr(preprocess,
                       camel_to_underscores(name))(data))
                gu.save_dataframe(new_df,name+dataFileName)
            
    return fea_df

def get_code(data):
    return pd.DataFrame.from_dict({"CodeLines": data["BodyMarkdown"].apply(code_lines)})

def reopen(df,num_days=14):
    if "PostClosedDate" not in df:
        raise KeyError
    df["PostClosedDate"] = df["PostClosedDate"].apply(gu.parse_date_maybe_null)
    df = reopen(df,num_days=14)
    time_delta = dt.timedelta(days=num_days)
    delta_date = df["PostClosedDate"] - df["PostCreationDate"]
    index = df[(df["OpenStatus"] != "open") & (delta_date <= dt.timedelta(days=14))].index
    df["OpenStatus"].ix[index] = "open"
    df["PostClosedDate"].ix[index] = np.nan
    return df

def preprocess(file_name="train-sample.csv"):
    # Build default dataframe and update column set with derived column data
    
    df = gu.build_dataframe(file_name)
    df = df.join(get_code(df)) # Separate code from body and join title with body
    df["BodyMarkdown"] = data["BodyMarkdown"].apply(text_lines) # Remove code from body text
    
    # Prepend title to body text and remove title column
    df["BodyMarkdown"] = df["Title"] + "\n" + df["BodyMarkdown"]
    del df["Title"]

    df = reopen(df,num_days=14) # Reopen questions that were closed more than 2 weeks after being asked

    


if __name__=="__main__":
    code_functions = [ "NumLinesCode"
                     , "LenLinesCode"
                     ]
    text_functions = [ "NumParagraphs"
                     , "NumSentences"
                     ]
    
    
    # Build & update dataframes for training data & test_data
    # gu.build_dataframe("train-sample.csv")
    # gu.build_dataframe("public_leaderboard.csv")
    
    # Modify dataframe objects
    
    
    
    print 'Getting the initial data'
    data = cu.get_dataframe() # by default returns panda dataframe for "train-sample.csv"
    
    print 'Separating source code.'
    code = get_code(data)
    print 'Separating text.'
    text = get_text(data)
    
    print 'Processing source code features.'
    features = data.join(process_and_pickle(code_functions,code))
    print 'Processing text features.'
    features = features.join(process_and_pickle(text_functions,text))
    
    print features

