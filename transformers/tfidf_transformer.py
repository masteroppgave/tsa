from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfNegTransformer(TfidfVectorizer):
    def __init__(self, tokenizer=None, analyzer='word', ngram_range=(1, 1), max_df=1.0, min_df=1, use_idf=True, smooth_idf=True, sublinear_tf=False):
        super(TfidfNegTransformer, self).__init__(self, tokenizer=tokenizer, analyzer=analyzer, ngram_range=ngram_range,
            max_df=max_df, min_df=min_df, use_idf=use_idf, smooth_idf=smooth_idf, sublinear_tf=sublinear_tf)
	
	def fit(self, raw_documents, y=None):
		return super(TfidfNegTransformer, self).fit(self.filter(raw_documents), y)

	def fit_transform(self, raw_documents, y=None):
		return super(TfidfNegTransformer, self).fit_transform(self.filter(raw_documents), y)

	def transform(self, raw_tweets, **args):
		return super(TfidfNegTransformer, self).transform(tweets, **args)