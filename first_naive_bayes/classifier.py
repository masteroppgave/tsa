import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from preprocess import PreProcessor

class TrainClassifier():
    def __init__(self):
        self.preprocessor = PreProcessor()
        self.documents = []
        self.word_frequency_distribution = []
        self.word_features = []
        self.featuresets = []
        self.training_set = []
        self.testing_set = []
        self.twitter_counter = 0

    def load_text_corpus_and_save_to_documents(self, file, category):
        for entry in file.split('\n'):
            self.documents.append( (entry, category) )
            

    def save_positive_n_negative_corpus_to_documents(self, pos_corpus, neg_corpus):
        self.load_text_corpus_and_save_to_documents(pos_corpus, "pos")
        self.load_text_corpus_and_save_to_documents(neg_corpus, "neg")
        random.shuffle(self.documents)

    def load_corpus_and_save_to_documents(self, filename, category):
        with open(file_name, 'r') as tweet_file:
            for line in tweet_file:
                try:
                    self.documents.append( (self.preprocessor.preprocess(line), category) )
                except: 
                    continue

    def process_documents(self, allowed_word_types=["J","R","V"]):
        for document_tuple in self.documents:
            self.twitter_counter += 1
            print self.twitter_counter
            try:
                tuple_words = self.preprocessor.tokenize(document_tuple[0])
                pos = nltk.pos_tag(tuple_words)
                for w in pos:
                    if w[1][0] in allowed_word_types:
                        self.word_frequency_distribution.append(w[0].lower())
            except:
                continue
        save_documents = open("pickled_algos/documents.pickle","wb")
        pickle.dump(self.documents, save_documents)
        save_documents.close()
        self.word_frequency_distribution = nltk.FreqDist(self.word_frequency_distribution)
        self.word_features = list(self.word_frequency_distribution.keys())[:3000]
        save_word_features = open("pickled_algos/word_features5k.pickle","wb")
        pickle.dump(self.word_features, save_word_features)
        save_word_features.close()
        

    def find_features(self, document):
        words = self.preprocessor.tokenize(document)
        features = {}
        for word in self.word_features:
            features[word] = (word in words)
        return features

    def initialize_featuresets(self):
        docs = self.documents
        featuresets = [(self.find_features(rev), category) for (rev, category) in docs]
        random.shuffle(featuresets)
        save_featuresets = open("pickled_algos/featuresets.pickle","wb")
        pickle.dump(featuresets, save_featuresets)
        save_featuresets.close()
        return featuresets
   

    def process_corpora_into_featuresets(self):
        self.process_documents()
        self.featuresets = self.initialize_featuresets()
        self.training_set = self.featuresets[:1000]
        self.testing_set = self.featuresets[1000:]

    def train_and_save_all_classifiers(self):
        self.NB_classifier = nltk.NaiveBayesClassifier.train(self.training_set)
        save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
        pickle.dump(self.NB_classifier, save_classifier)
        save_classifier.close()
        
        self.MNB_classifier = SklearnClassifier(MultinomialNB())
        self.MNB_classifier.train(self.training_set)
        save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
        pickle.dump(self.MNB_classifier, save_classifier)
        save_classifier.close()

        self.BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        self.BernoulliNB_classifier.train(self.training_set)
        save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
        pickle.dump(self.BernoulliNB_classifier, save_classifier)
        save_classifier.close()

        self.LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        self.LogisticRegression_classifier.train(self.training_set)
        save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
        pickle.dump(self.LogisticRegression_classifier, save_classifier)
        save_classifier.close()

        self.LinearSVC_classifier = SklearnClassifier(LinearSVC())
        self.LinearSVC_classifier.train(self.training_set)
        save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
        pickle.dump(self.LinearSVC_classifier, save_classifier)
        save_classifier.close()

        self.SGDC_classifier = SklearnClassifier(SGDClassifier())
        self.SGDC_classifier.train(self.training_set)
        save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
        pickle.dump(self.SGDC_classifier, save_classifier)
        save_classifier.close()

    def load_classifiers():
        try:
            NB_classifier_f = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
            self.NB_classifier = pickle.load(NB_classifier_f)
            NB_classifier_f.close()

            MNB_classifier_f = open("pickled_algos/MNB_classifier5k.pickle", "rb")
            self.MNB_classifier = pickle.load(MNB_classifier_f)
            MNB_classifier_f.close()

            BernoulliNB_classifier_f = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
            self.BernoulliNB_classifier = pickle.load(BernoulliNB_classifier_f)
            BernoulliNB_classifier_f.close()

            LogisticRegression_classifier_f = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
            self.LogisticRegression_classifier = pickle.load(LogisticRegression_classifier_f)
            LogisticRegression_classifier_f.close()

            LinearSVC_classifier_f = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
            self.LinearSVC_classifier = pickle.load(LinearSVC_classifier_f)
            LinearSVC_classifier_f.close()

            SGDC_classifier_f = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
            self.SGDC_classifier = pickle.load(SGDC_classifier_f)
            SGDC_classifier_f.close()
        except Exception, e:
            print str(e)



    def train_NB_classifier(self):
        self.NB_classifier = nltk.NaiveBayesClassifier.train(self.training_set)
        #print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
        
        save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
        pickle.dump(self.NB_classifier, save_classifier)
        save_classifier.close()
    
    def train_MNB_classifier(self):
        self.MNB_classifier = SklearnClassifier(MultinomialNB())
        self.MNB_classifier.train(selftraining_set)
        #print("self.MNB_classifier accuracy percent:", (nltk.classify.accuracy(self.MNB_classifier, testing_set))*100)
        
        save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
        pickle.dump(self.MNB_classifier, save_classifier)
        save_classifier.close()

    def train_BernoulliNB_classifier(self):
        self.BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        self.BernoulliNB_classifier.train(self.training_set)
        #print("self.BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(self.BernoulliNB_classifier, testing_set))*100)
        save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
        pickle.dump(self.BernoulliNB_classifier, save_classifier)
        save_classifier.close()

    def train_LogisticRegression_classifier(self):
        self.LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        self.LogisticRegression_classifier.train(self.training_set)
        #print("self.LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(self.LogisticRegression_classifier, testing_set))*100)

        save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
        pickle.dump(self.LogisticRegression_classifier, save_classifier)
        save_classifier.close()

    def train_LinearSVC_classifier(self):
        self.LinearSVC_classifier = SklearnClassifier(LinearSVC())
        self.LinearSVC_classifier.train(self.training_set)

        save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
        pickle.dump(self.LinearSVC_classifier, save_classifier)
        save_classifier.close()

    def train_SGDC_classifier(self):
        self.SGDC_classifier = SklearnClassifier(SGDClassifier())
        self.SGDC_classifier.train(self.training_set)

        save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
        pickle.dump(self.SGDC_classifier, save_classifier)
        save_classifier.close()

    def show_stats_NB_classifier(self):
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(self.NB_classifier, self.testing_set))*100)

    def show_stats_MNB_classifier(self):
        print("self.MNB_classifier accuracy percent:", (nltk.classify.accuracy(self.MNB_classifier, self.testing_set))*100)

    def show_stats_BernoulliNB_classifier(self):
        print("self.BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(self.BernoulliNB_classifier, self.testing_set))*100)

    def show_stats_LogisticRegression_classifier(self):
        print("self.LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(self.LogisticRegression_classifier, self.testing_set))*100)

    def show_stats_LinearSVC_classifier(self):
        print("self.LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(self.LinearSVC_classifier, self.testing_set))*100)

    def show_stats_SGDC_classifier(self):
        print("SGDClassifier accuracy percent:",nltk.classify.accuracy(self.SGDC_classifier, self.testing_set)*100)

    def show_stats_all_classifier_statistics(self): 
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(self.NB_classifier, self.testing_set))*100)
        print("self.MNB_classifier accuracy percent:", (nltk.classify.accuracy(self.MNB_classifier, self.testing_set))*100)
        print("self.BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(self.BernoulliNB_classifier, self.testing_set))*100)
        print("self.LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(self.LogisticRegression_classifier, self.testing_set))*100)
        print("self.LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(self.LinearSVC_classifier, self.testing_set))*100)
        print("SGDClassifier accuracy percent:",nltk.classify.accuracy(self.SGDC_classifier, self.testing_set)*100)
    
    

if __name__ == "__main__":
    short_pos = open("positive.txt","r").read()
    short_neg = open("negative.txt","r").read()
    classifier = TrainClassifier()
    classifier.save_positive_n_negative_corpus_to_documents(short_pos, short_neg)
    classifier.process_corpora_into_featuresets()
    classifier.train_and_save_all_classifiers()
    classifier.show_stats_all_classifier_statistics()