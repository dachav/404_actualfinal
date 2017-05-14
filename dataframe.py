import MySQLdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database_operations import *
from pylab import *
from numpy import *
from numpy.random import *
from scipy.stats import *


def get_df():
	i = 1
	#Establish a MySQL connection
	db = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql")
	cuisines = get_categories()
	for cuisine in cuisines:
	        sql = "select avg(w.sentiment) AS 'Average Sentiment', avg(w.rating) AS 'Average Rating', count(distinct w.rid) as 'Num Rest', count(*) as 'Num Ratings' from reviews w, rest r WHERE w.rid = r.rid AND categories LIKE '%" + cuisine + "%';"
	        if i > 1:
	            data = pd.read_sql_query(sql, db)
	            data = data.rename(index={0: cuisine})
	            df = pd.concat([df,data])
	            i+=1
	        else:
	            df = pd.read_sql_query(sql, db)
	            df = df.rename(index={0: cuisine})
	            i+=1
	return df
def do_regression(y, x):
	df = get_df()

	slope,intercept,r_value,p_value,slope_std_error = stats.linregress(df[x],df[y]) 

	y_modeled = df[x]*slope + intercept

	equation = y + ' = ' + str(round(slope,4)) + "*" + x + ' + ' + str(round(intercept,2)) + ' p-value = ' + str(round(p_value,2))

	plot(df[x], y_modeled,'-r',linewidth=1)
	plot(df[x], df[y],'ob',markersize=2)
	plt.ylabel(y)
	plt.xlabel(x)
	title = y + " vs. " + x
	plt.title(equation)
	plt.show()


do_regression('Average Sentiment','Average Rating')
do_regression('Average Sentiment','Num Rest')
do_regression('Average Rating','Num Ratings')
do_regression('Average Rating','Num Rest')

df = get_df()
d = dict()

db = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql")
cuisines = get_categories()
for cuisine in cuisines:
        sent_sql = "select w.sentiment, w.rating from reviews w, rest r WHERE w.rid = r.rid AND categories LIKE '%" + cuisine + "%';"
        data = pd.read_sql_query(sent_sql, db)
        sent = data['sentiment']
        rate = data['rating']
        raw_sent = list(sent)
        raw_rate = list(rate)
        
        d[cuisine] = raw_rate
        #d[cuisine] = raw_sent
        
F, p =  stats.f_oneway(d["Salvadoran"], d["Street Vendors"], d["Tapas/Small Plates"], d["Buffets"], d["Gluten-Free"], d["Sandwiches"], d["Creperies"], d["Argentine"], d["Tea Rooms"], d["Dim Sum"], d["French"], d["Dive Bars"], d["Thai"], d["Juice Bars & Smoothies"], d["Restaurants"], d["Karaoke"], d["Grocery"], d["Dominican"], d["Filipino"], d["Patisserie/Cake Shop"], d["Food Delivery Services"], d["Cocktail Bars"], d["Food Tours"], d["Imported Food"], d["Italian"], d["Steakhouses"], d["Mediterranean"], d["Desserts"], d["Delis"], d["Puerto Rican"], d["Halal"], d["Senegalese"], d["Noodles"], d["Tex-Mex"], d["Caribbean"], d["Dance Clubs"], d["American (New)"], d["Caterers"], d["Breakfast & Brunch"], d["Beer"], d["Food Stands"], d["Indonesian"], d["Hawaiian"], d["Coffee & Tea"], d["Cheesesteaks"], d["Tapas Bars"], d["Bubble Tea"], d["Szechuan"], d["Sushi Bars"], d["Lounges"], d["Persian/Iranian"], d["Fish & Chips"], d["Cuban"], d["Cajun/Creole"], d["Cafes"], d["Scandinavian"], d["Greek"], d["Burmese"], d["African"], d["Beer Bar"], d["Bars"], d["Kebab"], d["Burgers"], d["Asian Fusion"], d["Ethiopian"], d["Food Trucks"], d["Performing Arts"], d["Hookah Bars"], d["Middle Eastern"], d["Bangladeshi"], d["Indian"], d["Latin American"], d["Chicken Wings"], d["Korean"], d["Pakistani"], d["Wine & Spirits"], d["Barbeque"], d["Empanadas"], d["Southern"], d["Vegan"], d["Pubs"], d["Diners"], d["Sports Bars"], d["New Mexican Cuisine"], d["Gastropubs"], d["Afghan"], d["Seafood Markets"], d["Cooking Classes"], d["Bakeries"], d["Vegetarian"], d["Breweries"], d["Chicken Shop"], d["Irish"], d["Chinese"], d["Taiwanese"], d["Peruvian"], d["Wine Bars"], d["Basque"], d["Vietnamese"], d["Pool Halls"], d["Bagels"], d["Fast Food"], d["Venezuelan"], d["Colombian"], d["Food Court"], d["Cideries"], d["Salad"], d["Himalayan/Nepalese"], d["Pizza"], d["Venues & Event Spaces"], d["Music Venues"], d["Specialty Food"], d["Seafood"], d["Soup"], d["Convenience Stores"], d["Comfort Food"], d["Portuguese"], d["South African"], d["Mexican"], d["Popcorn Shops"], d["Colleges & Universities"], d["American (Traditional)"], d["Japanese"], d["International Grocery"], d["Hot Dogs"], d["Spanish"], d["Cafeteria"], d["Soul Food"])
        
print df.sort_values(['Average Rating'], ascending = False)     
        

