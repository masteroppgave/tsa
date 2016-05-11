from data import resources
import csv

def _nrc_emotion():
		lexicon_file = resources.lexica['nrc_e']
		with open(lexicon_file, mode='r') as f: 
			lines = f.readlines()[46:]
			reader = csv.reader(lines, delimiter='\t')
		lexicon = {}
		for row in reader:
			if int(row[2]) == 1:
				if row[1] == 'positive':
					lexicon[row[0]] = 1
				elif row[1] == 'negative':
					lexicon[row[0]] = -1
		return lexicon

def _bing_liu():
	lexicon = {}
	pos_lexicon_file = resources.lexica['bing_p']
	with open(pos_lexicon_file, mode='r') as f: 
		for word in f.readlines()[35:]:
			lexicon[word.strip()] = 1
	neg_lexicon_file = resources.lexica['bing_n']
	with open(neg_lexicon_file, mode='r') as f: 
		for word in f.readlines()[35:]:
			lexicon[word.strip()] = -1
	return lexicon

def _mpqa():
	lexicon = {}
	lexicon_file = resources.lexica['mpqa']
	with open(lexicon_file, mode='r') as f:  
		reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
		for row in reader:
			if row[5].split("=", 1)[1] == 'positive':
				if row[0].split("=", 1)[1] == 'strongsubj':
					lexicon[row[2].split("=", 1)[1]] = 2
				else:
					lexicon[row[2].split("=", 1)[1]] = 1
			elif row[5].split("=", 1)[1] == 'negative':
				if row[0].split("=", 1)[1] == 'strongsubj':
					lexicon[row[2].split("=", 1)[1]] = -2
				else:
					lexicon[row[2].split("=", 1)[1]] = -1
	return lexicon

if __name__ == "__main__":
	print _mpqa()