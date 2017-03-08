#!flask/bin/python
from app import app

#app.run("localhost", 5000, debug=True)
app.run('0.0.0.0', 5000, debug=False, threaded=True)
