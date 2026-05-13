# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')




@app.route('/users')
def display_users():
	# Query the database for the users
	users_list = execute_query("""
		SELECT    CREATORS.ID AS ID, CREATORS.Name AS Name, COUNT(HACK_AUTHOR.HackID) AS Count
		FROM      CREATORS
		LEFT JOIN HACK_AUTHOR ON HACK_AUTHOR.UserID=CREATORS.ID
		GROUP BY  CREATORS.ID
	""")
	return render_template('display_users.html', users = users_list)


@app.route('/location/<lat>,<lon>')
def display_user(lat,lon):
	# Query the database
	radius=.0145*3 # ~~ 3 mile
	rows = execute_query("""
		SELECT FOUNTAIN.ID, FOUNTAIN.Lat, FOUNTAIN.Lon
		FROM   FOUNTAIN
		WHERE  (FOUNTAIN.Lat-%f)*(FOUNTAIN.Lat-%f)+(FOUNTAIN.Lon-%f)*(FOUNTAIN.Lon-%f) < %f
	""" % (float(lat), float(lat), float(lon), float(lon), float(radius)))
	return render_template('location.html', lat=lat, lon=lon, nearby=[])



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
