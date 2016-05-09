negation_list = [
    "No",
    "Not",
    "None",
    "No one",
    "Noone"
    "Nobody",
    "Nothing",
    "Neither",
    "Nowhere",
    "Never",
    "no",
    "not",
    "none",
    "no one",
    "noone"
    "nobody",
    "nothing",
    "neither",
    "nowhere",
    "never",
]

negation_cues = ['hardly', 'lack', 'lacking', 'lacks', 'neither', 'nor', 'never', 'no', 'nobody', 'none',
                         'nothing', 'nowhere', 'not', 'without', 'aint', 'cant', 'cannot', 'darent', 'dont', 'doesnt',
                         'didnt', 'hadnt', 'hasnt', 'havent', 'havnt', 'isnt', 'mightnt', 'mustnt', 'neednt', 'oughtnt',
                         'shant', 'shouldnt', 'wasnt', 'wouldnt', ".*n't"]

class NegationLibrary(object):
	def __init__(self, negations=negation_list):
		self.negations = negation_list
        self.negation_cues = negation_cues
