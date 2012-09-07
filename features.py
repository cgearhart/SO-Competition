import competition_utilities as cu
import csv
import datetime
import features
import numpy as np
import pandas as pd
import re

def camel_to_underscores(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

##############################################################
###### FEATURE FUNCTIONS
##############################################################

def body_length(data):
    # returns a dataframe with the number of characters in the text
    return data["BodyMarkdown"].apply(len)

def num_tags(data):
    # complicated way to count the number of non-null values in columns that match "Tag%d" prototype in each row
    return pd.DataFrame.from_dict({"NumTags": [sum(map(lambda x:
                    pd.isnull(x), row)) for row in (data[["Tag%d" % d
                    for d in range(1,6)]].values)] } ) ["NumTags"]

def title_length(data):
    # returns a dataframe with the number of characters in the text
    return data["Title"].apply(len)

def user_age(data):
    # how many seconds between account creation and post creation
    return pd.DataFrame.from_dict({"UserAge": (data["PostCreationDate"]
            - data["OwnerCreationDate"]).apply(lambda x: x.total_seconds())})

###########################################################

def extract_features(feature_names, data):
    fea = pd.DataFrame(index=data.index) # creates a dataframe object with the same number of rows as "data"
    for name in feature_names:
        if name in data:
            # the feature name was already in the CSV file
            fea = fea.join(data[name])
        else:
            # use the functions above with the same feature name to calculate the requested value
            fea = fea.join(getattr(features,
                camel_to_underscores(name))(data)) # interesting note: "features" refers to the file, not the variable in __main__; i'm not entirely sure why - except that the definition of the order of precidence dictates that the file has highest precedence in the namespace at this point in the program
    return fea

if __name__=="__main__":
    feature_names = [ "BodyLength"
                    , "NumTags"
                    , "OwnerUndeletedAnswerCountAtPostTime"
                    , "ReputationAtPostCreation"
                    , "TitleLength"
                    , "UserAge"
                    ]
              
    data = cu.get_dataframe() # by default returns panda dataframe for "train-sample.csv"
    features = extract_features(feature_names, data)
    print(features)