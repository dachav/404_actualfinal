import xlrd
import MySQLdb

# Open the workbook and define the worksheet
book = xlrd.open_workbook("/Users/dchavez/Desktop/final project/restaurant.xlsx")
sheet = book.sheet_by_name("restaurant")

# Establish a MySQL connection
database = MySQLdb.connect(host="localhost", user = "root", passwd = "ilikeit", db = "mysql")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

#create tables
drop = "DROP TABLE Reviews;"
create = "CREATE TABLE Reviews (rid int PRIMARY KEY, id int, name varchar(100), categories varchar(100), price varchar(12), address longtext,phonenumber varchar(20) NULL, numberofreviews int, averagerating int, link varchar(100));"

cursor.execute(drop)
cursor.execute(create)



# Create the INSERT INTO sql query
query = """INSERT INTO Reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      rid      = sheet.cell(r,0).value
      id      = sheet.cell(r,1).value
      name          = sheet.cell(r,2).value
      cat     = sheet.cell(r,3).value
      price       = sheet.cell(r,4).value
      address = sheet.cell(r,5).value
      phone        = sheet.cell(r,6).value
      numRev       = sheet.cell(r,7).value
      avgRev     = sheet.cell(r,8).value
      link        = sheet.cell(r,9).value


      # Assign values from each row
      values = (rid, id, name, cat, price, address, phone, numRev, avgRev, link)

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print "Imported " , columns , " columns and " , rows , " rows to MySQL!"
