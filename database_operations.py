import MySQLdb
from textblob import TextBlob

#gets list of cuisine types
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
#gets number of restuarants given a cuisines
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
#gets average rating of restuarants given a cuisines
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
#gets number of reviews of restuarants given a cuisines
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
#gets row number and reviews given a cuisines
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

#get reviews and row given a cuisine where rating was 5 stars and sentiment > .6
def get_good_reviews():
      reviews = list()
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT row, review FROM Rest r, Reviews v WHERE r.rid = v.rid and v.rating = 5 and v.sentiment > .6 ORDER BY v.row"
      try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                  reviews.append([row[0], row[1]])
            return reviews
      except:
            db.rollback()
#get reviews and row given a cuisine where rating was 1 star and sentiment < 0

def get_bad_reviews():
      reviews = list()
      db = MySQLdb.connect("localhost","root","ilikeit", "mysql")
      cursor = db.cursor()
      sql = "SELECT row, review FROM Rest r, Reviews v WHERE r.rid = v.rid and v.rating = 1 and v.sentiment < 0 ORDER BY v.row"
      try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                  reviews.append([row[0], row[1]])
            return reviews
      except:
            db.rollback()

#gets sentiment score given text
def get_sentiment(text):
      text = text.decode('ascii', 'replace')
      blob = TextBlob(text)
      return blob.sentiment.polarity

#gets sentiment score given text
def get_avg_sentiment(genre):
      sentiment = list()
      reviews = get_reviews(genre)
      for review in reviews:
            sentiment.append(get_sentiment(review[1]))
      average = sum(sentiment) / float(len(sentiment))
      return average

#gets average sentiment of restuarants given a cuisines
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
#adds sentiment score to mysql table
def add_sentiment():
      # Establish a MySQL connection
      database = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql", use_unicode=True, charset="utf8")

      # Get the cursor, which is used to traverse the database, line by line
      cursor = database.cursor()

      cuisines = get_categories()

      for cuisine in cuisines:
            reviews = get_reviews(cuisine)
            for review in reviews:
                  sentiment = get_sentiment(review[1])
                  row = int(review[0])
                  sql = "UPDATE Reviews SET sentiment = " + str(sentiment) +  " WHERE row = " + str(row) + ";"
                  cursor.execute(sql)
      # Close the cursor
      cursor.close()
      # Commit the transaction
      database.commit()
      # Close the database connection
      database.close()




