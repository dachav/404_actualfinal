from database_operations import *
from textblob import TextBlob
import pandas as pd
import operator

#finds 20 noun phrases in text and returns phrase and occurance
def review_phrases(rev_lst):
	word_dict = dict()

	for review in rev_lst:
		text = review[1].lower()
		text = text.decode('ascii', 'replace')
		rev = TextBlob(text)
		words = rev.noun_phrases
		for word in words:
			if "i" in word:
				continue
			if word in word_dict.keys():
				word_dict[word] += 1
			else:
				word_dict[word] = 1


	sorted_words = sorted(word_dict.items(), key=lambda kv: kv[1], reverse=True)

	return sorted_words[:20]

#gets reviews phrases
top_20_good = review_phrases(get_good_reviews())
top_20_tapas = review_phrases(get_reviews('Tapas'))
top_20_bad = review_phrases(get_bad_reviews())

#prints phrases
print "The following phrases were used most frequently in good reviews\n"
for rev in top_20_good:
        print "'" + str(rev[0]) + "'" + " frequency: " + str(rev[1])

print "\nThe following phrases were used most frequently in bad reviews\n"
for rev in top_20_bad:
        print "'" + str(rev[0]) + "'" + " frequency: " + str(rev[1])

print "\nThe following phrases were used most frequently in reviews for tapas places\n"
for rev in top_20_tapas:
        print "'" + str(rev[0]) + "'" + " frequency: " + str(rev[1])
