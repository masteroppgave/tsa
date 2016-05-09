import json
from nltk.tokenize import word_tokenize
import re
import operator 
from nltk.corpus import stopwords
import string
from replacers import RegexpReplacer
from nltk import bigrams
from collections import defaultdict
from negations import NegationLibrary
from pprint import pprint
import codecs


class PreProcessor(object):
    def __init__(self):
        self.punctuation = list(string.punctuation)
        self.emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]
        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+self.emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
        self.stop_word_list = self.initialize_stop_word_list()
        self.contraction_expander = RegexpReplacer()

    def preprocess(self, string_object, remove_stop_words=False):
        if isinstance(string_object, dict):
            string_text = string_object["text"]
        else:
            # Assume type is string
            string_text = string_object
        string_text = codecs.encode(string_text, "utf-8")
        print string_text
        string_text = string_text.lower() #all tekst til smaa bokstaver
        string_text = self.contraction_expander.expand(string_text) #utvider forkortelser som didnt til did not
        string_text = string_text.strip('\'"') #fjerner unodvendig whitespace
        string_text = self.replace_two_or_more_letters(string_text) #fjerner for mange forekomster av samme tegn
        string_text = re.sub('@[^\s]+','',string_text) #fjerner alle  @mentions
        #string_text = re.sub('@[^\s]+','AT_USER',string_text) #bytter @mentions med "AT_USER"
        #string_text = re.sub(r'#([^\s]+)', r'\1', string_text) #bytter "#hashtag" med "hashtag"
        string_text = re.sub('[^A-Za-z0-9 ]+', '', string_text) #fjerner alle tegn som ikke er i alfabetet eller tall, eller space
        if remove_stop_words:
            string_text = ' '.join(filter(lambda word: word not in self.stop_word_list, string_text.split()))
        return string_text

    def initialize_stop_word_list(self, with_negation=True):
        stop_word_list = stopwords.words('english') + self.punctuation + ['rt', 'via']
        stop_word_list.append('AT_USER')
        stop_word_list.append('URL')
        negation_library = NegationLibrary()
        if (with_negation):
            for word in negation_library.negations:
                word_lower = word.lower()
                if word_lower in stop_word_list:
                    stop_word_list.remove(word_lower)
        return stop_word_list

    def tokenize(self, string_text, lowercase=True):
        tokens = self.tokens_re.findall(string_text)
        if lowercase:
            tokens = [token if (self.emoticon_re.search(token) and re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", token) is None) else token.lower() for token in tokens]
        return tokens

    def replace_two_or_more_letters(self, string_text):
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", string_text)

    def get_feature_vector(self, text_list):
        feature_vector = []
        tokenized_string_set = []
        for text in text_list:
            tokenized_list = self.tokenize(text)
            tokenized_string_set.append(tokenized_list)
            for token in tokenized_list:
                if token in self.stop_word_list:
                    continue
                else:
                    feature_vector.append(token)
        return feature_vector, tokenized_string_set

    def extract_features(self, string_text):
        word_set = set(string_text)
        features = {}
        for word in feature_list:
            features['contains(%s)' % word] = (word in word_set)
        return features

    def save_tweet_file_to_string_list(self, file_name):
        text_list = []
        with open(file_name, 'r') as tweet_file:
            for line in tweet_file:
                tweet = json.loads(line)
                tweet_text = tweet["text"]
                text_list.append(tweet_text)
        return text_list

    def preprocess_string_list(self, text_list):
        processed_string_list = []
        for text in text_list: 
            processed_string_text = self.preprocess(text)
            processed_string_list.append(processed_string_text)
        return processed_string_list



#################
## RUN PROGRAM ##
#################

if __name__ == "__main__":
    preprocessor = PreProcessor()
    file_name = 'tweets1.json'
    all_tweets = preprocessor.save_tweet_file_to_string_list(file_name)
    all_tweets_processed = preprocessor.preprocess_string_list(all_tweets)
    print all_tweets_processed
    raw_input()
    feature_list, tokenized_tweets = preprocessor.get_feature_vector(all_tweets_processed)
    for tweet in all_tweets_processed:
        pprint(preprocessor.extract_features(tweet))



