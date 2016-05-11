import csv
import re
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import normalize
from data import lexicons
import numpy as np

class LexiconTransformer(TransformerMixin, BaseEstimator):
	def __init__(self, unigrams=True, bigrams=False, norm=False):
		self.unigrams = unigrams
		self.bigrams = bigrams
		self.normalize = norm
		self.nrc = lexicons._nrc_emotion
		self.bingliu = lexicons._bing_liu
		self.mpqa = lexicons._mpqa
	
	def transform(self, raw_tweets, y=None):
		#matrix = np.zeros((len(raw_tweets), 4))
		manual_lexica = [self.nrc, self.bingliu, self.mpqa]
		for lexicon in manual_lexica:
			matrix = self._manual_lexicon_scorer(raw_tweets, lexicon())
		return matrix

	def fit(self, raw_tweets, y=None):
		return self

	def _manual_lexicon_scorer(self, raw_tweets, lexicon_dict):
		scores = np.zeros((len(raw_tweets), 4))
		negation_re = r'(.*)_NEG(?:FIRST)?$'
		for i, contexts in enumerate(raw_tweets):
			for token in contexts.split(" "):
				try:
					if re.match(negation_re, token):
						print "found token: %s" % (token)
						token = re.sub(negation_re, r'\1', token)
						scores[i][2 if lexicon_dict[token] > 0 else 3] += lexicon_dict[token]
					else:
						scores[i][0 if lexicon_dict[token] > 0 else 1] += lexicon_dict[token]
				except KeyError:
					pass
		return normalize(scores) if self.normalize else scores
