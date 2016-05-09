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
    "Never"
]

class NegationLibrary(object):
	def __init__(self, negations=negation_list):
		self.negations = negation_list
