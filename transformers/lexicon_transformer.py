import csv
import re
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import normalize
from data import resources
import numpy as np

class LexiconTransformer(TransformerMixin, BaseEstimator):
	def __init__(self, unigrams=True, bigrams=False, norm=True):
		self.unigrams = unigrams
		self.bigrams = bigrams
		self.normalize = norm

	def _nrc_emotion(self):
		lexicon_file = resources.lexica['nrc_e']
		with open(lexicon_file, mode='r') as f: # parameter for open():  ,encoding='utf-8'
			lines = f.readlines()[46:]
			reader = csv.reader(lines, delimiter='\t')
		lexicon = {}
		for row in reader:
			if int(row[2]) == 1:
				if row[1] == 'positive':
					lexicon[row[0]] = 1
				elif row[1] == 'negative':
					lexicon[row[0]] = -1
		return lexicon

	def _bing_liu(self):
		lexicon = {}
		pos_lexicon_file = resources.lexica['bing_p']
		with open(pos_lexicon_file, mode='r') as f: # parameter for open(): encoding='latin-1'
			count = 1
			for word in f.readlines()[35:]:
				if count == 1:
					print word
				lexicon[word.strip()] = 1
		neg_lexicon_file = resources.lexica['bing_n']
		with open(neg_lexicon_file, mode='r') as f: # parameter for open(): encoding='latin-1'
			for word in f.readlines()[35:]:
				lexicon[word.strip()] = -1
		return lexicon
	
	def _mpqa(self):
		lexicon = {}
		lexicon_file = resources.lexica['mpqa']
		with open(lexicon_file, mode='r') as f:  # parameter for open(): encoding='latin-1'
			reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
			for row in reader:
				if row[5].split("=", 1)[1] == 'positive':
					if row[0].split("=", 1)[1] == 'strongsubj':
						lexicon[row[2].split("=", 1)[1]] = 2
					else:
						lexicon[row[2].split("=", 1)[1]] = 1
				elif row[5].split("=", 1)[1] == 'negative':
					if row[0].split("=", 1)[1] == 'strongsubj':
						lexicon[row[2].split("=", 1)[1]] = -2
					else:
						lexicon[row[2].split("=", 1)[1]] = -1
		return lexicon
	
	def transform(self, raw_tweets, y=None):
		#matrix = np.zeros((len(raw_tweets), 4))
		manual_lexica = [self._nrc_emotion, self._bing_liu, self._mpqa]
		for lexicon in manual_lexica:
			matrix = self._manual_lexicon_scorer(raw_tweets, lexicon())
		return matrix

	def _manual_lexicon_scorer(self, raw_tweets, lexicon_dict):
		scores = np.zeros((len(raw_tweets), 4))
		for i, contexts in enumerate(raw_tweets):
			for token in contexts:
				try:
					negation_regex = r'(.*)_NEG(?:FIRST)?$'
					if re.match(negation_regex, token):
						token = re.sub(negation_regex, r'\1', token)
						scores[i][2 if lexicon_dict[token] > 0 else 3] += lexicon_dict[token]
					else:
						scores[i][0 if lexicon_dict[token] > 0 else 1] += lexicon_dict[token]
				except KeyError:
					pass
		return normalize(scores) if self.normalize else scores