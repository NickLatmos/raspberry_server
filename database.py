import MySQLdb

hostname = 'localhost'
username = 'root'
password = '1000641253'
database = 'WEATHER'

def connectToSQLDatabase():
	print 'Using MySQL - library'
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
		#Order: ID, DATE, TIME, TEMPERATURE, HUMIDITY 
		if tableName == "MEASUREMENTS":
			query = "INSERT INTO %s VALUES (\'%s\', CURDATE(), CURTIME(), %s, %s)" \
			% (tableName, dataList[0], dataList[1], dataList[2])
		else:
			query = ""
	except (RuntimeError, TypeError, NameError):
		print "An error occured while building the query for inserting data"
		query = ""
		pass

	print(query)
	return query

#Select the last measurement in the database for a specific device
def getLatestMeasurementQuery(device_id):
	query = '''SELECT MEASUREMENT_DATE, MEASUREMENT_TIME, TEMPERATURE, HUMIDITY 
						 FROM MEASUREMENTS 
						 WHERE MEASUREMENT_DATE=(SELECT MEASUREMENT_DATE 
																		 FROM MEASUREMENTS 
																		 ORDER BY MEASUREMENT_DATE DESC 
																		 LIMIT 1) AND DEVICE_ID=\'%s\' 
						 ORDER BY MEASUREMENT_TIME DESC
						 LIMIT 1;''' % (device_id)
	return query

#Checks if the device asking for data exists
#for security reasons.
def checkIfValidDeviceID(conn, device_id):
	query = "SELECT ID FROM DEVICE WHERE ID=\'%s\';" % device_id
	rows = runQuery(conn,query);
	if not rows:
		return False
	else:
		return True

#Count the total rows in the table
def countRows(conn, tableName):
	query = "SELECT COUNT(*) FROM %s;" % tableName
	cur = conn.cursor()
	cur.execute("USE %s;" % database)
	cur.execute(query)
	conn.commit
	numOfRows = cur.fetchmany(size=1)
	return numOfRows





