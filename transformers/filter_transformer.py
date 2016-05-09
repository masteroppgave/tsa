import re
import numpy as np

from sklearn.base import TransformerMixin, BaseEstimator
import utils.filters as f

class FilterTransformer(TransformerMixin, BaseEstimator):        

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, data):
        for tweet in data: 
            f.remove_all_filters(tweet)
        return data