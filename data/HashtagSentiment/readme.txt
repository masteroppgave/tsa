NRC HashtagSentiment Lexicons
Version 2.0
26 September 2014
Copyright (C) 2014 National Research Council Canada (NRC)
Contact: Saif Mohammad (saif.mohammad@nrc-cnrc.gc.ca)

**********************************************
TERMS OF USE
**********************************************

1. This copy of the NRC HashtagSentiment Lexicons is to be used for research purposes only.  Please contact NRC if interested in a commercial license.

2. Do not redistribute the NRC HashtagSentiment Lexicons. Please refer interested parties to Saif Mohammad (saif.mohammad@nrc-cnrc.gc.ca).

3. When publishing results of research that used NRC HashtagSentiment Lexicons, please acknowledge their use and cite the following publication:
Kiritchenko, S., Zhu, X., Mohammad, S. (2014). Sentiment Analysis of Short Informal Texts. Journal of Artificial Intelligence Research, 50:723-762, 2014.


**********************************************
DATA SOURCE
**********************************************

The NRC HashtagSentiment Lexicons are automatically generated from the following data source: 
775,000 tweets with sentiment-word hashtags collected by NRC.


**********************************************
FILE FORMAT
**********************************************

Each line in the lexicons has the following format:
<term><tab><score><tab><Npos><tab><Nneg>

<term> can be a unigram or a bigram;
<score> is a real-valued sentiment score: score = PMI(w, pos) - PMI(w, neg), where PMI stands for Point-wise Mutual Information between a term w and the positive/negative class;
<Npos> is the number of times the term appears in the positive class, ie. in tweets with positive hashtag or emoticon;
<Nneg> is the number of times the term appears in the negative class, ie. in tweets with negative hashtag or emoticon.


**********************************************
AffLex and NegLex
**********************************************

Both parts, AffLex and NegLex, of each lexicon are contained in the same file. The NegLex entries have suffixes '_NEG' or '_NEGFIRST'.

In the unigram lexicon:
'_NEGFIRST' is attached to terms that directly follow a negator;
'_NEG' is attached to all other terms in negated contexts (not directly following a negator).

In the bigram lexicon:
'_NEG' is attached to all terms in negated contexts.

Both suffixes are attached only to nouns, verbs, adjectives, and adverbs. All other parts of speech do not get these suffixes attached. 


**********************************************
More Information
**********************************************
Details on the process of creating the lexicons can be found in:
Kiritchenko, S., Zhu, X., Mohammad, S. (2014). Sentiment Analysis of Short Informal Texts.  Journal of Artificial Intelligence Research, 50:723-762, 2014.

 
