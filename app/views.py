from app import app

#The views are the handlers that respond to requests from web 
#browsers or other clients. In Flask handlers are written 
#as Python functions. Each view function is mapped to 
#one or more request URLs.
@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Nick'}  # fake user
	return '''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Hello, ''' + user['nickname'] + '''</h1>
  </body>
</html>
'''