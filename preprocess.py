import competition_utilities as cu
import pandas as pd
import re

##############################################################
###### INCLUSION TEST FUNCTIONS
##############################################################

def code_lines(text):
    return ''.join([line for line in text if line.startswith(('\t','    '))])

def text_lines(text):
    return ''.join([line for line in text if not line.startswith(('\t','    '))])

##############################################################
###### DATA PROCESSING FUNCTIONS
##############################################################

def split_DFtext(data,name="BodyMarkdown",inclusion_test_fn=lambda x: x):
    data[name] = data["BodyMarkdown"].apply(inclusion_test_fn)
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

