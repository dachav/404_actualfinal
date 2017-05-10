import MySQLdb
from textblob import TextBlob

def get_categories():
      categories = list()
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT DISTINCT categories FROM Rest WHERE NOT categories LIKE '%Wrong%'"
      try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                  rest_cat = row[0][1:].strip().split(", ")
                  for rec in rest_cat:
                        if rec not in categories:
                              categories.append(rec)
            sort_cat = sorted(categories)
            return sort_cat
      except:
            db.rollback()

def num_rest(genre):
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT count(*) FROM Rest WHERE categories LIKE '%" + genre + "%'"
      try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return int(result[0])
      except:
            db.rollback()

def avg_rating(genre):
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT AVG(v.rating) FROM Rest r, Reviews v WHERE r.rid = v.rid and categories LIKE '%" + genre + "%'"
      try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return float(result[0])
      except:
            db.rollback()

def num_reviews(genre):
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT Count(*) FROM Rest r, Reviews v WHERE r.rid = v.rid and categories LIKE '%" + genre + "%'"
      try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return float(result[0])
      except:
            db.rollback()

def get_reviews(genre):
      reviews = list()
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT row, review FROM Rest r, Reviews v WHERE r.rid = v.rid and categories LIKE '%" + genre + "%' ORDER BY v.row"
      try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                  reviews.append([row[0], row[1]])
            return reviews
      except:
            db.rollback()

def get_sentiment(text):
      text = text.decode('ascii', 'replace')
      blob = TextBlob(text)
      return blob.sentiment.polarity

def get_avg_sentiment(genre):
      sentiment = list()
      reviews = get_reviews(genre)
      for review in reviews:
            sentiment.append(get_sentiment(review[1]))
      average = sum(sentiment) / float(len(sentiment))
      return average

def get_ratings_row(row):
      ratings = list()
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT rating FROM Rest r, Reviews v WHERE r.rid = v.rid and row =" + str(row)
      try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return float(result[0])
      except:
            db.rollback()

#code below get sentiment and yelp rating
 
##rev = []
##test = get_categories()
##reviews = get_reviews("Wine")
##for review in reviews:
##      test = review[1]
##      rev.append([get_sentiment(test), get_ratings_row(int(review[0]))])
##for view in rev:
##      print view
##      

print get_avg_sentiment("Wine")


