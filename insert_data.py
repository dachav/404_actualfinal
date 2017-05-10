import xlrd
import MySQLdb
import datetime

# Open the workbook and define the worksheet
book1 = xlrd.open_workbook("/Users/dchavez/Desktop/final project/restaurant.xlsx")
sheet1 = book1.sheet_by_name("restaurant")
book2 = xlrd.open_workbook("/Users/dchavez/Desktop/final project/review.xlsx")
sheet2 = book2.sheet_by_name("review")

# Establish a MySQL connection
database = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql", use_unicode=True, charset="utf8")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

#create tables
drop2 = "DROP TABLE Reviews;"
drop1 = "DROP TABLE Rest;"
create1 = "CREATE TABLE Rest (rid int PRIMARY KEY, id int, name varchar(100), categories varchar(100), price varchar(12), address longtext,phonenumber varchar(20) NULL, numberofreviews int, averagerating int, link varchar(100));"
create2 = "CREATE TABLE Reviews(row bigint, rid int, user_name varchar(50), user_city varchar(100),num_friends int,num_reviews int,rating int, date date, useful int,funny int,cool int,review longtext,CONSTRAINT pk_rid_name PRIMARY KEY (row), CONSTRAINT fk_rev_rest FOREIGN KEY (rid)REFERENCES  Rest(rid));"

cursor.execute(drop2)
cursor.execute(drop1)
cursor.execute(create1)
cursor.execute(create2)



# Create the INSERT INTO sql query
query1 = """INSERT INTO Rest VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
query2 = """INSERT INTO Reviews VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet1.nrows):
      rid      = sheet1.cell(r,0).value
      id      = sheet1.cell(r,1).value
      name          = sheet1.cell(r,2).value
      cat     = sheet1.cell(r,3).value
      price       = sheet1.cell(r,4).value
      address = sheet1.cell(r,5).value
      phone        = sheet1.cell(r,6).value
      numRev       = sheet1.cell(r,7).value
      avgRev     = sheet1.cell(r,8).value
      link        = sheet1.cell(r,9).value


      # Assign values from each row
      values1 = (rid, id, name, cat, price, address, phone, numRev, avgRev, link)

      # Execute sql Query
      cursor.execute(query1, values1)
# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet2.nrows):
      row = r
      rid      = sheet2.cell(r,0).value
      user_name      = sheet2.cell(r,1).value
      user_city          = sheet2.cell(r,2).value
      num_friends       = sheet2.cell(r,3).value
      num_reviews = sheet2.cell(r,4).value
      rating        = sheet2.cell(r,5).value
      
      ms_date_number = sheet2.cell(r, 6).value # Correct option 2

      year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number, book2.datemode)
      date = datetime.datetime(year, month, day)

      useful     = sheet2.cell(r,7).value
      funny        = sheet2.cell(r,8).value
      cool        = sheet2.cell(r,9).value
      review        = sheet2.cell(r,10).value


      # Assign values from each row
      values2 = (row, rid, user_name, user_city, num_friends, num_reviews, rating, date, useful, funny, cool, review)

      # Execute sql Query
      cursor.execute(query2, values2)


# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done! Bye, for now."
print ""
columns = str(sheet1.ncols)
rows = str(sheet1.nrows)
print "I just imported " , columns , " columns and " , rows , " rows to MySQL!"
