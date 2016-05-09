from utils import filters
from sklearn.preprocessing import normalize


def transform(raw_tweets):
		vectorized = []
		for tweet in raw_tweets:
			happy = float(len(filters.Happy_RE.findall(tweet)))
			sad = float(len(filters.Sad_RE.findall(tweet)))
			vectorized.append([happy, sad])
		return normalize(vectorized)