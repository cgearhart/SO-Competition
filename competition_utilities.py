from __future__ import division
from collections import Counter
from gearley_utilities import *
import csv
import dateutil
import numpy as np
import os
import pandas as pd


if not data_path or not submissions_path:
    raise Exception("Set the data and submission paths in competition_utilities.py!")

def get_reader(file_name="train-sample.csv"):
    reader = csv.reader(open(os.path.join(data_path, file_name)))
    header = reader.next()
    return reader

def get_header(file_name="train-sample.csv"):
    reader = csv.reader(open(os.path.join(data_path, file_name)))
    header = reader.next()
    return header

def get_closed_count(file_name):
    return sum(1 for q in iter_closed_questions(file_name))

def iter_closed_questions(file_name):
    df_iter = pd.io.parsers.read_csv(os.path.join(data_path, file_name), iterator=True, chunksize=1000)
    return (question[1] for df in df_iter for question in df[df["OpenStatus"] != "open"].iterrows())

def iter_open_questions(file_name):
    df_iter = pd.io.parsers.read_csv(os.path.join(data_path, file_name), iterator=True, chunksize=1000)
    return (question[1] for df in df_iter for question in df[df["OpenStatus"] == "open"].iterrows())

def get_priors(file_name):
    # seems to return the naive probability that an arbitrary post will be closed
    # for each specific reason; it returns a list of global averages
    closed_reasons = [r[14] for r in get_reader(file_name)]
    closed_reason_counts = Counter(closed_reasons)
    reasons = sorted(closed_reason_counts.keys())
    total = len(closed_reasons)
    priors = [closed_reason_counts[reason]/total for reason in reasons]
    return priors

def update_prior(old_prior,  old_posterior, new_prior):
    evidence_ratio = (old_prior*(1-old_posterior)) / (old_posterior*(1-old_prior))
    new_posterior = new_prior / (new_prior + (1-new_prior)*evidence_ratio)
    return new_posterior

def cap_and_update_priors(old_priors, old_posteriors, new_priors, epsilon):
    old_posteriors = cap_predictions(old_posteriors, epsilon)
    old_priors = np.kron(np.ones((np.size(old_posteriors, 0), 1)), old_priors) # converts a list to an np.array (supports vector operations)
    new_priors = np.kron(np.ones((np.size(old_posteriors, 0), 1)), new_priors)
    evidence_ratio = (old_priors*(1-old_posteriors)) / (old_posteriors*(1-old_priors))
    new_posteriors = new_priors / (new_priors + (1-new_priors)*evidence_ratio)
    new_posteriors = cap_predictions(new_posteriors, epsilon)
    return new_posteriors

def cap_predictions(probs, epsilon):
    # this is the multiclass log-loss function implementation
    probs[probs>1-epsilon] = 1-epsilon
    probs[probs<epsilon] = epsilon
    row_sums = probs.sum(axis=1)
    probs = probs / row_sums[:, np.newaxis]
    return probs

def write_submission(file_name, predictions):
    writer = csv.writer(open(os.path.join(submissions_path, file_name), "w"), lineterminator="\n")
    writer.writerows(predictions)

if __name__=='__main__':
    get_dataframe()

