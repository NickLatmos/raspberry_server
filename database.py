import MySQLdb

hostname = 'localhost'
username = 'root'
password = '1000641253'
database = 'testDB'

def connectToSQLDatabase():
	print 'Using MySQL - lib'
	conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database)
	return conn

def runQuery(conn, query):
	rows = ""
	try:
		cur = conn.cursor()
		cur.execute("USE %s;" % database)
		cur.execute(query)
		#Important to commit the data
		conn.commit()
		rows = cur.fetchall()
		for row in rows:
			print row
	except:
		conn.rollback()
		print "Something went wrong. Rollback to previous state"
	return rows

#Returns an insert sql command.
def buildInsertQuery(dataList, tableName):
	try:
		if tableName == "MEASUREMENTS":
			query = "INSERT INTO %s (TEMPERATURE, HUMIDITY) VALUES (%s, %s)" % (tableName, dataList[0], dataList[1])
		elif tableName == "NEW_MEASUREMENTS":
			query = "INSERT INTO %s VALUES (\'%s\', CURDATE(), CURTIME(), %s, %s)" % (tableName, dataList[0], dataList[1], dataList[2])
		else:
			query = ""
	except (RuntimeError, TypeError, NameError):
		print "An error occured while building the query for inserting data"
		query = ""
		pass

	print(query)
	return query

#Select the last measurement in the database for a specific place
def getLatestMeasurementQuery(place):
	query = '''SELECT PLACE, MEASUREMENT_TIME, TEMPERATURE, HUMIDITY 
						 FROM NEW_MEASUREMENTS 
						 WHERE MEASUREMENT_DATE=(SELECT MEASUREMENT_DATE 
																		 FROM NEW_MEASUREMENTS 
																		 ORDER BY MEASUREMENT_DATE DESC 
																		 LIMIT 1) AND PLACE=\'%s\' 
						 ORDER BY MEASUREMENT_TIME DESC
						 LIMIT 1;''' % (place)
	return query

#Count the total rows in the table
def countRows(conn, tableName):
	query = "SELECT COUNT(*) FROM %s;" % tableName
	cur = conn.cursor()
	cur.execute("USE %s;" % database)
	cur.execute(query)
	conn.commit
	numOfRows = cur.fetchmany(size=1)
	return numOfRows

#Count the total rows in the table for a specific place
def countRowsInSpecificPlace(conn, tableName, place):
	query = "SELECT COUNT(*) FROM %s WHERE PLACE=\'%s\';" % (tableName, place)
	cur = conn.cursor()
	cur.execute("USE %s;" % database)
	cur.execute(query)
	conn.commit
	numOfRows = cur.fetchmany(size=1)
	return numOfRows




