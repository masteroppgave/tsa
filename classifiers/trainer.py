import pickle

from time import time

import numpy as np
from sklearn.metrics import f1_score, make_scorer, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit, StratifiedKFold
from sklearn.preprocessing import StandardScaler

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from transformers.emoticon_transformer import *
from transformers.tfidf_transformer import *
from transformers.lexicon_transformer import *

from data import resources


def train_classifier(classifier=None, training_set=None, label_set=None, force_new=0):
	classifier_type, classifier_name = get_classifier(classifier)
	classifier_path = os.path.join(resources.pickles, classifier_name+'.pickle')
	if os.path.exists(classifier_path) and not force_new:
		with open(classifier_path, 'rb') as file:
			pipeline = pickle.load(file)
	else:
		stratified_split = StratifiedShuffleSplit(label_set, 1, 0.2, random_state=1)
		for train_indices, test_indices in stratified_split:
			X_train = [training_set[train_index] for train_index in train_indices]
			X_test = [training_set[test_index] for test_index in test_indices]
			y_train = [label_set[train_index] for train_index in train_indices]
			y_test = [label_set[test_index] for test_index in test_indices]

	# X = [elem[0] for elem in training_set]
	# y = [elem[1] for elem in training_set]
	# X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

	filter_transformer = Pipeline([
			('filter', FilterTransformer())
		])

	tfidf_parameters = {'use_idf': 1,
							'smooth_idf': 1,
							'sublinear_tf': 1,
							'norm': 'l2',
							'stop_words': 'english',
							'lowercase': True,
							'max_features': 3000}

	feature_union = FeatureUnion([
		('tfidf', TfidfNegTransformer(analyser='word', ngram_range=(1,4), **tfidf_parameters)),
		('lex', LexiconTransformer(norm=True)),
		('emoticons', EmoticonTransformer(norm=True))
	])

	pipeline_config = resources.config['pipeline']
	pipeline = Pipeline([
		('preprocessing', filter_transformer),
		('feature_extraction', feature_union),
		('scaler', StandardScaler(with_mean=False))
		('clf', classifier_type)])

	

	return pipeline

def get_classifier(argument):
	return {
		"linearsvm": LinearSVC(),
		"svm": SVC(),
		"maxent": LogisticRegression(),
		"nb": MultinomialNB()
	}.get(argument, LinearSVC()), argument

def grid_search(feature_pipeline, X_train, y_train):
	grid_search_config = resources.config['grid_search']
	parameters = {
		'clf__kernel': grid_config['SVMKernel'].split(','),
		'clf__C': np.linspace(float(grid_config['CStart']),
			float(grid_config['CEnd']),
			num=int(grid_config['CNumber'])),
		'clf__gamma': np.linspace(float(grid_config['GammaStart']),
			float(grid_config['GammaEnd']),
			num=int(grid_config['GammaNumber'])),
	}
	grid_search = GridSearchCV(
		feature_pipeline,
		param_grid=parameters,
		scoring=make_scorer(f1_score, labels=['positive', 'neutral', 'negative'], average='macro'),
		cv=StratifiedKFold(y_train, 10, shuffle=True),
		n_jobs=int(resources.config['parallel']['n_jobs']),
		verbose=10
	)
	start = time()
	grid_search.fit(X_train, y_train)
	print("Performed SVM grid search in %0.3fs" % (time() - t0))
	print("Best grid search CV score: {:0.3f}".format(grid_search.best_score_))
	print("Best parameters set:")

	best_parameters = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
		print("\t%s: %r" % (param_name, best_parameters[param_name]))
	pipeline = grid_search.best_estimator_

	with open(os.path.join(resources.pickles, 'grid_scores.pickle'), 'wb') as f:
		pickle.dump(grid_search.grid_scores_, f)

	return pipeline