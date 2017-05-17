from database_operations import *
from textblob import TextBlob
import pandas as pd
import operator


def review_phrases(rev_lst):
	word_dict = dict()

	for review in rev_lst:
		text = review[1].lower()
		text = text.decode('ascii', 'replace')
		rev = TextBlob(text)
		words = rev.noun_phrases
		for word in words:
			if word in word_dict.keys():
				word_dict[word] += 1
			else:
				word_dict[word] = 1


	sorted_words = sorted(word_dict.items(), key=operator.itemgetter(1))

	return sorted_words

print review_phrases(get_good_reviews())[-20:]
print review_phrases(get_reviews('Tapas'))[-20:]
print review_phrases(get_bad_reviews())[-20:]
