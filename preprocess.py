import competition_utilities as cu
import pandas as pd
import re
import ngram
from functools import partial

##############################################################
###### INCLUSION TEST FUNCTIONS
##############################################################

def code_lines(md):
    return ''.join([line for line in md if line.startswith(('\t','    '))])

def text_lines(md):
    return ''.join([line for line in md if not line.startswith(('\t','    '))])

def paragraph_count(md):
    return md.count('\n\n')

def sentence_count(md):
    pass

def code_lines_count(md):
    return md.count('\n')

def code_lines_length(md):
    return [len(line) for line in md]

def words_per_code_line(md):
    return [line.lstrip().count(' ') for line in md]

def ngram_wrapper(fn,nValue):
    return partial(fn,nValue)

def ngram(nValue,md):
    pass
          
""" example ngram usage:
    
    for i in range(3):
        ngram_fn = ngram_wrapper(ngram,i)
        split_DFtext(data,'{}gram'.format(i),ngram_fn)
    
"""


##############################################################
###### DATA PROCESSING FUNCTIONS
##############################################################

def split_DFtext(data,name="BodyMarkdown",inclusion_test_fn=lambda x: x):
    data[name] = data["BodyMarkdown"].apply(inclusion_test_fn) # this creates a new DF object with heading specified by "name"
    return data[name]

###########################################################

def process_and_pickle(function_list,data):
    text_stats = pd.DataFrame(index=BodyMarkdown.index) # creates a dataframe object with rows matched to "data"
    code_stats = pd.DataFrame(index=BodyMarkdown.index)
    for name in text_functions:
        text_stats = text_stats.join(getattr(preprocess,name)(BodyMarkdown))
    for name in code_functions:
        code_stats = text_stats.join(getattr(preprocess,name)(BodyMarkdown))
    return stats

if __name__=="__main__":
    function_names = [ ''
                     ]
              
    data = cu.get_dataframe() # by default returns panda dataframe for "train-sample.csv"
    
    print data.shape
    
    a = split_DFtext(data,'text',text_lines)
    b=a.ix[0]
    print b.splitlines()

