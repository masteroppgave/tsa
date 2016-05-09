from utils import filters
from sklearn.preprocessing import normalize
from sklearn.base import TransformerMixin, BaseEstimator

class EmoticonTransformer(TransformerMixin, BaseEstimator):
	def __init__(self, norm=True):
		self.norm = norm

	def contains_emoticon(self, token):
		return bool(Emoticon_RE.match(token))

	def contains_happy_emoticon(self, token):
		return bool(Happy_RE.match(token))

	def contains_sad_emoticon(self, token):
		return bool(Sad_RE.match(token))

	def transform(self, raw_tweets):
		vectorized = []
		for tweet in raw_tweets:
			number_of_happy_emoticons = float(len(filters.Happy_RE.findall(tweet)))
			number_of_sad_emoticons = float(len(filters.Sad_RE.findall(tweet)))
			vectorized.append([number_of_happy_emoticons, number_of_sad_emoticons])
		return normalize(vectorized) if self.norm else vectorized

	def fit(self, raw_tweets, y=None):
		return self