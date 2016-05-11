import re
from negation_replacer import NegationReplacer
from nltk.corpus import stopwords
from negations import NegationLibrary
import string
import HTMLParser


stopwords = stopwords.words('english') + list(string.punctuation) + ['rt', 'via']

# Regex for different emoticons
NormalEyes = r'[:=8]'
HappyEyes = r'[xX]'
Wink = r'[;]'
NoseArea = r'[\*\-o\Oc\^\']?'
HappyMouths = r'[D\)\]\3\>\d\}]'
SadMouths = r'[\(\[]'
Tongues = r'[pP]'
BigTongue = r'[P]'
SmallTongue = r'[p]'
OtherMouths = r'[doO/\\]'

Happy = (
	"(" + NormalEyes + "|" + Wink + "|" + HappyEyes + ")" + NoseArea + HappyMouths 
)
Happy_RE = re.compile(Happy, re.UNICODE)
Sad_RE = re.compile(NormalEyes + NoseArea + SadMouths,  re.UNICODE)

Wink_RE = re.compile(Wink + NoseArea + HappyMouths,  re.UNICODE)
Tongue_RE = re.compile(NormalEyes + NoseArea + Tongues,  re.UNICODE)
Other_RE = re.compile('(' + NormalEyes + '|' + Wink + ')' + NoseArea + OtherMouths, re.UNICODE)

Emoticon = (
	"(" + NormalEyes + "|" + Wink + ")" + NoseArea +
	"(" + Tongues + "|" + OtherMouths + "|" + SadMouths + "|" + HappyMouths + ")"
)
Emoticon_RE = re.compile(Emoticon,  re.UNICODE)

#usernames
usernames = r'(@[a-zA-Z0-9_]{1,15})'

# retweets
retweet = r'(^RT\s+|\s+RT\s+)'

#hashtags
hashtags = re.compile(r'(#[a-zA-Z]+[a-zA-Z0-9_]*)')

contraction_expander = NegationReplacer()

def remove_all_filters(string_text):
	temp = HTMLParser.HTMLParser().unescape(string_text)
	temp = replace_two_or_more_letters(string_text)
	temp = remove_user_mentions(string_text)
	temp = expand_negations(string_text)
	temp = remove_whitespace(string_text)
	temp = replace_hashtags_with_words(string_text)
	temp = remove_strange_symbols(string_text)
	return temp

def remove_emoticons(string_text):
	tweet = re.sub(Happy_RE, "", string_text)
	tweet = re.sub(Sad_RE, "", tweet)
	tweet = re.sub(Emoticon_RE, "", tweet)
	return tweet.lower().strip()

def expand_negations(string_text):
	return contraction_expander.expand(string_text) #utvider forkortelser som didnt til did not

def replace_username(string_text):
	return re.sub('@[^\s]+','AT_USER',string_text) #bytter @mentions med "AT_USER"

def remove_whitespace(string_text):
	pattern = re.compile(r'\s')
	string_text = re.sub(pattern,' ',string_text)
	return string_text.strip('\'"') #fjerner unodvendig whitespace

def replace_two_or_more_letters(string_text):
	pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	return pattern.sub(r"\1\1", string_text)

def remove_user_mentions(string_text):
	return re.sub('@[^\s]+','',string_text) #fjerner alle  @mentions

def replace_hashtags_with_words(string_text):
	return re.sub(r'#([^\s]+)', r'\1 '+r'#\1', string_text) #bytter "#hashtag" med "hashtag #hashtag"

def remove_strange_symbols(string_text):
	return re.sub('[^A-Za-z0-9 _+-.,!@#$%^&*();\/\\:?=|<>"\']', '', string_text) #fjerner alle tegn er fremmede for vanlig vestlig tekstlig data

def remove_stop_words(string_text):
	return ' '.join(filter(lambda word: word not in stopwords, string_text.split()))

def remove_negations(string_text):
	return ' '.join(filter(lambda word: word not in negation_library.negations, string_text.split()))