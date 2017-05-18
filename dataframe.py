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

        

