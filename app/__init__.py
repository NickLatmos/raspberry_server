from flask import Flask
from flask import request
from flask import json
from random import randint
import datetime
import clientHandler 
import json 
import database 


app = Flask(__name__)
from app import views

measurementsTable = "MEASUREMENTS"

@app.route('/postdata', methods = ['POST'])
def postJsonHandler():
    print str(request.headers)
    requestType = request.headers['content-type']

    #Check if data are in Json format
    if requestType == "application/json":
    	    #returns a json format
            content = json.dumps(request.json)
            print "The server received the following data\n" + str(content)

	    #convert the json format into a dictionary
	    contentDictionary = json.loads(content)
	    
	    #device id, temperature, humidity
	    device_id = contentDictionary["id"]
	    temperature = contentDictionary["Temperature"]
	    humidity = contentDictionary["Humidity"]
	    pressure = contentDictionary["Pressure"]
	    case_temperature = contentDictionary["Case Temperature"]
	    weather = contentDictionary["Weather"]

	    #insert the posted data into the SQL table
	    conn = database.connectToSQLDatabase()
	    if database.checkIfValidDeviceID(conn, device_id):
	    	#Insert the data in the database
		    data = [device_id, temperature, humidity, pressure, case_temperature, weather]
		    query = database.buildInsertQuery(data, measurementsTable)
		    database.runQuery(conn, query)
	    else:
			content = "ID not valid"

	    conn.close()

    if requestType == "application/x-www-form-urlencoded":
            device_id = request.values.get("id")
            temperature = request.values.get("Temperature")
            humidity = request.values.get("Humidity")
            pressure = request.values.get("Pressure")
            case_temperature = request.values.get("Case Temperature")
            weather = request.values.get("Weather")
            
	    #insert the posted data into the SQL table
	    conn = database.connectToSQLDatabase()
	    if database.checkIfValidDeviceID(conn, device_id):
        	    #Insert the data in the database
                    print "ID valid"
		    data = [device_id, temperature, humidity, pressure, case_temperature, weather]
		    query = database.buildInsertQuery(data, measurementsTable)
		    database.runQuery(conn, query)
		    print "data inserted"
		    content = "Sucess!"
	    else:
       		content = "ID not valid"

	    conn.close()

    #Return something to the browser
    return 'Data posted\n' + str(content)

#----! Must change from ?id=xxx to ?place=xxx 
@app.route('/getrecentdata', methods = ['GET'])
def getJsonHandler():
	# here we want to get the value of user (i.e. ?id=some-value)
    device_id = request.args.get('id')
    print "A user asks for the most recent data from the device with id: " + device_id

	#getting the last measurement
    conn = database.connectToSQLDatabase()
    query = database.getLatestMeasurementQuery(device_id)
    rows = database.runQuery(conn, query)			#return a list
    conn.close()

    if not rows:
    	return "Not valid ID"
    else:
    	return '''Data found: 
    			<br>
    			<br>Date: %s
    			<br>Time of measurement: %s 
    			<br>Temperature: %s 
    			<br>Humidity: %s''' \
    			% (rows[0][0],rows[0][1],rows[0][2],rows[0][3])


@app.route('/valve', methods = ['GET'])
def valveHandler():
	# get the device's id.
    device_id = request.values.get('id')

    #insert the posted data into the SQL table
    conn = database.connectToSQLDatabase()
    if database.checkIfValidDeviceID(conn, device_id):
    	if randint(0,1):
    		command = "VALVE NO"
    	else:
    		command = "VALVE NC"
    	print command
    else:
		command = "ID not valid"

    conn.close();

    return command + '\r'

@app.route('/time', methods = ['GET'])
def getTime():
    now = datetime.datetime.now()				
    print "TIME %02d:%02d:%02d" % (now.hour, now.minute, now.second)
    return "TIME %02d:%02d:%02d%c" % (now.hour, now.minute, now.second, '\a')

@app.route('/date', methods = ['GET'])
def getDate():
    now = datetime.datetime.now()	
    print 'DATE %04d:%02d:%02d' % (now.year, now.month, now.day)			
    return 'DATE %04d:%02d:%02d%c' % (now.year, now.month, now.day, '\a')


#This thread is responsible for incoming TCP Socket connections
#This might be used for the GSM/GPRS solution
clientHandler.start_new_thread(clientHandler.startService, ())




