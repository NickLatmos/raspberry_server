from flask import Flask
from flask import request
from flask import json
from random import randint
import clientHandler 
import json 
import database 


app = Flask(__name__)
from app import views

measurementsTable = "MEASUREMENTS"

@app.route('/postdata', methods = ['POST'])
def postJsonHandler():
	#returns a json format
    content = json.dumps(request.json)
    print "The server received the following data\n" + str(content)

    requestType = request.headers['content-type']
    #Check if data are in Json format
    if requestType == "application/json":
	    #convert the json format into a dictionary
	    contentDictionary = json.loads(content)
	    
	    #device id, temperature, humidity
	    device_id = contentDictionary["id"]
	    temperature = contentDictionary["Temperature"]
	    humidity = contentDictionary["Humidity"]

	    #insert the posted data into the SQL table
	    conn = database.connectToSQLDatabase()
	    if database.checkIfValidDeviceID(conn, device_id):
	    	#Insert the data in the database
		    data = [device_id, temperature, humidity]
		    query = database.buildInsertQuery(data, measurementsTable)
		    database.runQuery(conn, query)
	    else:
			content = "ID not valid"

	    conn.close()

    #Return something to the browser
    return 'Return: \n' + str(content)


@app.route('/getrecentdata', methods = ['GET'])
def getJsonHandler():
	# here we want to get the value of user (i.e. ?place=some-value)
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
    device_id = request.args.get('id')

    #insert the posted data into the SQL table
    conn = database.connectToSQLDatabase()
    if database.checkIfValidDeviceID(conn, device_id):
    	if randint(0,1):
    		command = "{VO}"
    	else:
    		command = "{VC}"
    else:
		command = "ID not valid"

    conn.close();

    return command


#This thread is responsible for incoming TCP Socket connections
#This might be used for the GSM/GPRS solution
clientHandler.start_new_thread(clientHandler.startService, ())




