from __future__ import division
import os
import dateutil
import pandas as pd

# These path names need to be set for your system
data_path = os.path.join(os.path.expanduser("~"),"Projects/SO Datafiles")
submissions_path = os.path.join(os.path.expanduser("~"),"Projects/SO Outputs")
if not data_path or not submissions_path:
    raise Exception("Set the data and submission paths in gearley_utilities.py!")


df_converters = {"PostCreationDate": dateutil.parser.parse,
    "OwnerCreationDate": dateutil.parser.parse}#,
#"PostClosedDate": dateutil.parser.parse}

def parse_date_maybe_null(date):
    if date:
        return dateutil.parser.parse(date)
    return None


def build_dataframe(file_name="train-sample.csv"):
    # Force creation of dataframe from a csv file
    try:
        print "Building new dataframe from {}".format(file_name)
        df = pd.io.parsers.read_csv(os.path.join(data_path,file_name), converters=df_converters)
        df.save(pickle_path(file_name))
        return df
    except IOError,msg:
        print "Problem building dataframe.\n{}".format(msg)


def get_dataframe(file_name="train-sample.csv"):
    # Try loading dataframe from a pickle
    name_without_ext,ext = os.path.splitext(file_name)
    pickle_file = os.path.join(data_path,name_without_ext+".pickle")
    if os.path.exists(pickle_file):
        print "Loading a pickle named {}".format(name_without_ext+".pickle")
        return pd.load(pickle_file)
    else:
        raise IOError


def pickle_path(file_name="train-sample.csv"):
    name_without_ext,ext = os.path.splitext(file_name)
    return os.path.join(data_path,name_without_ext+".pickle")


if __name__=="__main__":
    # Data columns
    # PostId, PostCreationDate, OwnerUserId, OwnerCreationDate, ReputationAtPostCreation, OwnerUndeletedAnswerCountAtPostTime, Title, BodyMarkdown, Tag1, Tag2, Tag3, Tag4, Tag5, PostClosedDate, OpenStatus
    data = get_dataframe()
    
    open_data = data[data["OpenStatus"] == "open"]
    closed_data = data[data["OpenStatus"] != "open"]
    
