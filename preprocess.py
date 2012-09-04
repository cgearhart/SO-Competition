from __future__ import division
from collections import Counter
import string
import competition_utilities as cu
import pandas as pd
import re
from functools import partial

##############################################################
###### INCLUSION TEST FUNCTIONS
##############################################################

def code_lines(md):
    return '\n'.join([line.lstrip() for line in md.splitlines() if line.startswith(('\t','    '))]) # does not preserve indentation

def text_lines(md):
    return '\n'.join([line for line in md.splitlines() if not line.startswith(('\t','    ')) and len(line) > 0]) # non-empty lines that aren't indented

def paragraph_count(md):
    return md.count('\n')

def sentence_count(md):
    pass

def num_code_lines(md):
    return len(md.splitlines())

def code_lines_length(md):
    return [len(line) for line in md.splitlines()]

def ngram(nValue,md,head=True):
    md = md.translate(None,string.punctuation)
    if head:
        ngrams = [word[0:nValue] for word in md.split() if len(word) >= nValue]
    else:
        ngrams = [word[-nValue:] for word in md.split() if len(word) >= nValue]
    ngram_counts = Counter(ngrams)
    ngram_keys = sorted(ngram_counts.keys())
    total = len(ngrams)
    ngram_priors = [ngram_counts[ngram]/total for ngram in ngram_keys]
    return dict(zip(ngram_keys,ngram_priors))


##############################################################
###### DATA PROCESSING FUNCTIONS
##############################################################

def split_df_text(df_col_data,name="NewCol",test_fn=lambda x: x):
    data[name] = df_col_data.apply(test_fn) # this creates a new DF object with heading specified by "name"
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
    
    df_index = 1
    df_element = data["BodyMarkdown"].ix[df_index] # col/row indexing in a dataframe
    print ' '
    print 'BodyMarkdown:\n{}'.format(df_element)
    print '\n########################\n'
    
    # Test inclusion test functions
    textlines = text_lines(df_element)
    print 'TextLines:\n{}'.format(textlines)
    print '\n########################\n'
    codelines = code_lines(df_element)
    print 'CodeLines:\n{}'.format(codelines)
    print '\n########################\n'
    paragraphs = paragraph_count(textlines)
    print 'Paragraphs:\n{}'.format(paragraphs)
    #print '\n########################\n'
    #sentences = split_df_text(data,name="sentences",test_fn=sentence_count)
    #print 'Sentences:\n{}'.format(sentences[df_index])
    print '\n########################\n'
    numCodeLines = num_code_lines(codelines)
    print 'Lines of code:\n{}'.format(numCodeLines)
    print '\n########################\n'
    codeLinesLength = code_lines_length(codelines)
    print 'Length of code lines:\n{}'.format(codeLinesLength)
    print '\n########################\n'
    numCodeLines = num_code_lines(codelines)
    print 'Lines of code:\n{}'.format(numCodeLines)

    print '\n########################\n'
    print 'leading N-grams:'
    for i in range(2,5):
        ngram_fn = partial(ngram,i)
        print '\n########################\n'
        print 'i: {}\n'.format(i)
        print 'ngram\tprobability'
        for k,val in ngram_fn(textlines).iteritems():
            print '{}:\t{:.2f}'.format(k,val)
        
    print '\n########################\n'
    print 'trailing N-grams:'
    for i in range(2,5):
        ngram_fn = partial(ngram,i)
        print '\n########################\n'
        print 'i: {}\n'.format(i)
        print 'ngram\tprobability'
        for k,val in ngram_fn(textlines,head=False).iteritems():
            print '{}:\t{:.2f}'.format(k,val)