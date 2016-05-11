import re
import numpy as np

from sklearn.base import TransformerMixin, BaseEstimator
from utils import filters

class FilterTransformer(TransformerMixin, BaseEstimator):        
    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, data):
        for tweet in data: 
            filters.remove_all_filters(str(tweet))
        return data