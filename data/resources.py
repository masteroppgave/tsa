import configparser
import os

RESOURCES_DIR = os.path.dirname(__file__)

training_data = os.path.join(RESOURCES_DIR, 'tweets/labeled_tweets.tsv')

cleaned_data = os.path.join(RESOURCES_DIR, 'tweets/tweet_texts.txt')

lexica = {'s140_u': os.path.join(RESOURCES_DIR, 'Sentiment140/S140-AFFLEX-NEGLEX-unigrams.txt'),
          's140_b': os.path.join(RESOURCES_DIR, 'Sentiment140/S140-AFFLEX-NEGLEX-bigrams.txt'),
          'hs_u': os.path.join(RESOURCES_DIR, 'HashtagSentiment/HS-AFFLEX-NEGLEX-unigrams.txt'),
          'hs_b': os.path.join(RESOURCES_DIR, 'HashtagSentiment/HS-AFFLEX-NEGLEX-bigrams.txt'),
          'nrc_e': os.path.join(RESOURCES_DIR, 'NRC-Emotion-Lexicon-v0.92/'
                                               'NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt'),
          'bing_p': os.path.join(RESOURCES_DIR, 'BingLiu/positive-words.txt'),
          'bing_n': os.path.join(RESOURCES_DIR, 'BingLiu/negative-words.txt'),
          'mpqa': os.path.join(RESOURCES_DIR, 'MPQA/subjclueslen1-HLTEMNLP05.tff')
          }

pickles = os.path.join(RESOURCES_DIR, 'pickles')

config = configparser.ConfigParser()
config.read(os.path.join(RESOURCES_DIR, 'settings.conf'))
