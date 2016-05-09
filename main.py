import csv
import re

import numpy as np
import pandas as pd

from resources import resources




def load_data(training_file):
    """load data from csv"""
    training_data = None
    label_data = None
    if training_file:
        frame = pd.read_csv(training_file,
                            sep='\t',
                            names=['id', 'unknkown', 'label', 'text'],
                            na_values=['Not Available'],
                            converters={'label': lambda s: re.sub(r'objective.*|neutral.*', 'neutral', s)},
                            quoting=csv.QUOTE_NONE).dropna()
        n_samples = int(resources.config['data']['NumberOfSamples'])
        if n_samples > 0:
            frame = frame[:n_samples]
        training_data = np.array(frame['text'])
        label_data = np.array(frame['label'])
        print("Number of tweets in data set: {}".format(len(training_data)))
    return training_data, label_data



if __name__ == "__main__":
    training_set, label_set = load_data()