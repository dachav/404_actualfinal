#!/usr/bin/python
import pandas as pd
from dataframe import *
import MySQLdb
from scipy.stats import *
from database_operations import *

#addds sentiment to mysql
add_sentiment()

#plots regression of key variables in relation to cuisines
do_regression('Average Sentiment','Average Rating')
do_regression('Average Sentiment','Num Rest')
do_regression('Average Rating','Num Ratings')
do_regression('Average Rating','Num Rest')

#create a dataframe of the file
df = get_df()

#reviews greater than 20
df= df[df['Num Ratings'] > 20]

#find mean and sdev for each metric
analyze_these = ['Average Sentiment','Average Rating','Num Rest','Num Ratings']

for i in analyze_these:
	avg = df[i].mean()
	sdev = df[i].std()
	print i, "Avg: ", avg, "Sdev: ", sdev , "\n"

#computes average and st dev for rating and sentiment
avg_rating = df["Average Rating"].mean()
sdev_rating = df["Average Rating"].std()
avg_sent = df["Average Sentiment"].mean()
sdev_sent = df["Average Sentiment"].std()

#gets top 50% of ratings and sentiment by cuisine
df_top_rating =  df[df['Average Rating'] > avg_rating]
df_top_sent =  df[df['Average Sentiment'] > avg_rating]

#gets top 15 cuisines in average rating and average sentiment
df_top15_rating = df_top_rating.sort_values(['Average Rating'], ascending = False).head(15)
df_top15_sent = df_top_rating.sort_values(['Average Sentiment'], ascending = False).head(15)

print " \n top 15 cuisines by rating:"
print df_top15_rating

print " \n top 15 cuisines by sentiment:"
print df_top15_sent

#merges both dataframes to get cuisines
both = pd.merge(df_top15_rating, df_top15_sent, how='inner', on = ['Average Sentiment','Average Rating','Num Rest','Num Ratings'], left_index = True, right_index=True, sort=True)

print "\n Here are the cuisine types that appear in both the top 15 avg sentiment datframe and top 15 avg rating datframe:"
print both



#funtion to create a scoring method for rating and sentiment
def get_score(avg_r, avg_s):
	score = (.5 * avg_r) + (.5 * avg_s)
	return score
#creates score column
df['Score'] = get_score(df["Average Rating"], df["Average Sentiment"])

#creates df of just scores
df = df.sort_values(['Score'], ascending = False).head(10)
df_scores = df.iloc[:,-1]
print "\nTop 10 cuisines by score: "
print df_scores


drate = dict()
dsent = dict()
dscore = dict()
top_cuisines = list()

#runs anova test on rating, sentiment, and score on top cuisnes
top_rate_cuisines =  df_top15_rating.index.tolist()
top_sent_cuisines =  df_top15_sent.index.tolist()
top_score_cuisines =  df_scores.index.tolist()

top_cuisines.extend(top_rate_cuisines)
top_cuisines.extend(top_sent_cuisines)
top_cuisines.extend(top_score_cuisines)

db = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql")
for cuisine in top_cuisines:
        sent_sql = "select w.sentiment, w.rating from reviews w, rest r WHERE w.rid = r.rid AND categories LIKE '%" + cuisine + "%';"
        data = pd.read_sql_query(sent_sql, db)
        sent = data['sentiment']
        rate = data['rating']
        score = get_score(rate, sent)
        raw_sent = list(sent)
        raw_rate = list(rate)
        raw_score = list(score)
        
        drate[cuisine] = raw_rate
        dsent[cuisine] = raw_sent
        dscore[cuisine] = raw_score

F, p =  stats.f_oneway(drate["Senegalese"], drate["Popcorn Shops"], drate["Food Stands"], drate["Tapas/Small Plates"], drate["Cooking Classes"],drate["Halal"],drate["Coffee & Tea"],drate["Filipino"],drate["Peruvian"],drate["Persian/Iranian"],drate["Dive Bars"],drate["Spanish"],drate["Bagels"],drate["Greek"],drate["Tapas Bars"])

print "\nThe Following Results from ANOVA one-sided test for top rated cuisines\n"
print "F statistic: " + str(F) + ", p- value: " + str(p)

F, p =  stats.f_oneway(dsent["Cooking Classes"],dsent["Tapas Bars"],dsent["Spanish"],dsent["Senegalese"],dsent["Coffee & Tea"],dsent["Dive Bars"],dsent["Wine & Spirits"],dsent["Tapas/Small Plates"],dsent["Ethiopian"],dsent["Beer"],dsent["Gastropubs"],dsent["Beer Bar"],dsent["Cideries"],dsent["Cafes"],dsent["Breweries"],)

print "\nThe Following Results from ANOVA one-sided test for top average sentiment cuisines\n"
print "F statistic: " + str(F) + ", p- value: " + str(p)
F, p =  stats.f_oneway(dscore["Senegalese"], dscore["Popcorn Shops"], dscore["Cooking Classes"], dscore["Food Stands"], dscore["Tapas/Small Plates"],dscore["Coffee & Tea"],dscore["Halal"],dscore["Dive Bars"],dscore["Spanish"],dscore["Tapas Bars"])

print "\nThe Following Results from ANOVA one-sided test for top scores\n"
print "F statistic: " + str(F) + ", p- value: " + str(p)
