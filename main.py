import csv
import re
import os

import numpy as np
import pandas as pd

from data import resources
import utils.filters as f
from classifiers.trainer import *
from transformers.filter_transformer import *

def load_data(training_file):
    training_data, label_data = None, None
    if training_file:
        frame = pd.read_csv(training_file,
                            sep='\t',
                            names=['id', 'unknkown', 'label', 'text'],
                            na_values=['Not Available'],
                            converters={'label': lambda s: re.sub(r'objective.*|neutral.*', 'neutral', s)},
                            quoting=csv.QUOTE_NONE).dropna()
        training_data = np.array(frame['text'])
        label_data = np.array(frame['label'])
    return training_data, label_data

def train(training_data, label_data, classifier="svm"): 
    return train_classifier(classifier=classifier, training_set=training_data, label_set=label_data, force_new=1)


def classify(raw_data, classifier):
    preprocessed = [f.remove_all_filters(tweet) for tweet in raw_data]
    return classifier.predict(preprocessed)

if __name__ == "__main__":
    root_dir = os.path.dirname(__file__)
    data_file = os.path.join(root_dir, 'data/tweets/labeled_tweets.tsv')
    training_set, label_set = load_data(data_file)
    clf = train(training_set, label_set, classifier="nb")


"""
    "linearsvm": LinearSVC(),
    "svm": SVC(),
    "maxent": LogisticRegression(),
    "nb": MultinomialNB()
"""