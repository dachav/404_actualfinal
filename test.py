from database_operations import *
import MySQLdb
import pandas as pd
import numpy as np

db = MySQLdb.connect("localhost","root","ilikeit", "mysql")

cuisines = get_tag_categories('useful')


def get_restaurants():
	cursor = db.cursor()
	sql = "SELECT DISTINCT name FROM Rest WHERE rid IS NOT NULL"
	restaurants = list()
	try:
	    cursor.execute(sql)
	    result = cursor.fetchall()
	    for row in result:
	          restaurants.append(row[0])
	    return restaurants
	except:
		db.rollback()

rests = get_restaurants()

i = 1
for rest in rests:
    sql = "SELECT DISTINCT avg(w.sentiment) AS 'Average Sentiment', avg(w.rating) AS 'Average Rating', count(*) as 'Num Ratings' from reviews w, rest r WHERE w.rid = r.rid AND name LIKE '%" + str(rest) + "%';"
    if i > 1:
        data = pd.read_sql_query(sql, db)
        data = data.rename(index={0: rest})
        df = pd.concat([df,data])
        i+=1
    else:
        df = pd.read_sql_query(sql, db)
        df = df.rename(index={0: rest})
        i+=1


df = df.sort_values(['Average Sentiment'], ascending = False)
df = df.head(30)
top_places = df.index.tolist()

categories = dict()
rest_cat = list()
cursor2 = db.cursor()


for place in top_places:
	cats = "SELECT categories from Rest where name LIKE '%" + str(place) + "%';"
	try:
		cursor2.execute(cats)
		result2 = cursor2.fetchall()
		for row in result2:
			rest_cat = row[0][1:].strip().split(", ")
			for rec in rest_cat:
				if rec not in categories.keys():
					categories[rec] = 1
				else:
					categories[rec] += 1
	except:
		db.rollback()


print categories
                        


