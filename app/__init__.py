from flask import Flask
from flask import request
from flask import json
import clientHandler 
import json 
import database 

app = Flask(__name__)
from app import views

tableName = "NEW_MEASUREMENTS"

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
	  #returns a json format
    content = json.dumps(request.json)
    print "The server received the following data\n" + str(content)

    requestType = request.headers['content-type']
    #Check if data are in Json format
    if requestType == "application/json":
	    #convert the json format into a dictionary
	    contentDictionary = json.loads(content)
	    
	    #Find the data we want
	    place = contentDictionary["Place"]
	    temperature = contentDictionary["Temperature"]
	    humidity = contentDictionary["Humidity"]

	    #insert the posted data into the SQL table
	    conn = database.connectToSQLDatabase()
	    data = [place, temperature, humidity]
	    query = database.buildInsertQuery(data, tableName)
	    database.runQuery(conn, query)
	    conn.close()

    #Return something to the browser
    return 'JSON posted \n' + str(content)


@app.route('/getjson', methods = ['GET'])
def getJsonHandler():
		 # here we want to get the value of user (i.e. ?place=some-value)
    place = request.args.get('place')
    print place

	  #getting the temperature
    conn = database.connectToSQLDatabase()
    query = database.getLatestMeasurementQuery(place)
    rows = database.runQuery(conn, query)
    conn.close()

    return '''Data found:
    	<br>
    	<br>Place: %s
    	<br>Time of measurement: %s 
    	<br>Temperature: %s 
    	<br>Humidity: %s''' % (rows[0][0],rows[0][1],rows[0][2],rows[0][3])

#This thread is responsible for incoming TCP Socket connections
clientHandler.start_new_thread(clientHandler.startService, ())




