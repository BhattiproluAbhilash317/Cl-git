def break_words(stuff):
	"""This is going to break words"""
	words=stuff.split(' ')
	return words

def sort_words(words):
	"""this gives sorted words"""
	return sorted(words)
	
def print_first_word(words):
	"""prints first word"""
	word= words.pop(0)
	print words

def print_last_words(words):
	"""Prints the last word"""
	word=words.pop(-1)
	print words

def sort_sentence(sentence):
	"""Sortts the sentence"""
	word=break_words(sentence)
	return sort_words(words)

def print_first_last(sentence):
	"""Prints the first and last word"""
	words=break_words(sentence)
	print_first_word(words)
	print_last_word(words)

def print_first_last_sort(sentence):
	"""Prints the sorted sentence"""
	words=sort_sentence(sentence)
	print_first_word(words)
	print_last_word(words)

	