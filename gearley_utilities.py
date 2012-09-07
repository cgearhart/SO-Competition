import os
import pandas as pd


data_path = os.path.join(os.path.expanduser("~"),"Projects/SO Datafiles")
submissions_path = os.path.join(os.path.expanduser("~"),"Projects/SO Outputs")
if not data_path or not submissions_path:
    raise Exception("Set the data and submission paths in gearley_utilities.py!")


def get_dataframe(file_name="train-sample.csv",force_update=False):
    # update get_dataframe to try loading from a pickle before loading from CSV
    name_without_ext,ext = os.path.splitext(file_name)
    pickle_file = os.path.join(data_path,name_without_ext+".pickle")
    file_name = os.path.join(data_path,name_without_ext+".csv")
    if not force_update and os.path.exists(pickle_file):
        print "Loading a pickle named {}".format(name_without_ext+".pickle")
        return pd.load(pickle_file)
    elif os.path.exists(file_name):
        print "No pickle found, looking for a csv file named.".format(name_without_ext+".pickle")
        return pd.io.parsers.read_csv(os.path.join(data_path, file_name), converters = df_converters)
    else:
        raise IOError

def save_dataframe(df_obj,file_name):
    # save a dataframe object to a file specified by filename
    name_without_ext,ext = os.path.splitext(file_name)
    df_obj.save(os.path.join(data_path,name_without_ext+".pickle"))
    print "Pickled the df object {}".format(file_name)