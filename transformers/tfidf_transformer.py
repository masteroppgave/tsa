from sklearn.feature_extraction.text import TfidfVectorizer
from utils.negations import NegationLibrary
from utils import tokenizer


class TfidfNegTransformer(TfidfVectorizer):
	def __init__(self, negate=True, **kwargs):
		super(TfidfNegTransformer, self).__init__(self, **kwargs)
		self.negation_scope = negate
		self.negation_cues = NegationLibary().negations
	
	def fit(self, raw_documents):
		return super(TfidfNegTransformer, self).fit(self.process_negation_in_dataset(raw_documents), y)

	def fit_transform(self, raw_documents):
		return super(TfidfNegTransformer, self).fit_transform(self.process_negation_in_dataset(raw_documents), y)

	def transform(self, raw_documents, **kwargs):
		return super(TfidfNegTransformer, self).transform(self.process_negation_in_dataset(raw_documents), **kwargs)
	
	def process_negation_in_dataset(self, data):
		for tweet in data:
			append_negations_in_tweet(tweet)
		return data

	def append_negations_in_tweet(self, tweet):
		tokens = tokenizer.tokenize(tweet)
		for index in range(0,len(tokens)): 
			token = tokens[index]
			if self.negate:
				if token in self.negation_cues:
					if index-1 > 0 and index-1 < len(tokens)-1:
						tokens[index-1] += '_NEG'
						tokens[index] += '_NEG'
						tokens[index+1] += '_NEG'
					elif index+1 > len(tokens)-1:
						tokens[index-1] += '_NEG'
						tokens[index] += '_NEG'
					elif index-1 < 0:
						tokens[index] += '_NEG'
						tokens[index+1] += '_NEG'
					else:
						tokens[index] += '_NEG'
		return ' '.join(tokens)

