from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfNegTransformer(TfidfVectorizer):
	def __init__(self, negate=True, **kwargs):
		super(TfidfNegTransformer, self).__init__(self, **kwargs)

"""
	def fit(self, raw_tweets, y=None):
		return super(TfidfNegTransformer, self).fit(self.filter(raw_tweets), y)

	def fit_transform(self, raw_tweets, y=None):
		return super(TfidfNegTransformer, self).fit_transform(self.filter(raw_tweets), y)

	def transform(self, raw_tweets, **args):
		return super(TfidfNegTransformer, self).transform(raw_tweets, **args)
"""