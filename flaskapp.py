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



@app.route('/location/<lat>,<lon>')
def display_user(lat,lon):
	# Query the database
	radius=.0145*3 # ~~ 3 mile
	rows = execute_query("""
		SELECT FOUNTAIN.ID, FOUNTAIN.Lat, FOUNTAIN.Lon
		FROM   FOUNTAIN
		WHERE  (FOUNTAIN.Lat-(%f))*(FOUNTAIN.Lat-(%f))+(FOUNTAIN.Lon-(%f))*(FOUNTAIN.Lon-(%f)) < %f
	""" % (float(lat), float(lat), float(lon), float(lon), float(radius*radius)))

	fountains = []
	for row in rows:
		ftn = {}
		ftn['ID'] = row['ID']
		ftn['Lat'] = row['Lat']
		ftn['Lon'] = row['Lon']
		ftn['rating'] = execute_query("""
			SELECT AVG(RATING.Overall) AS Rating
			FROM   RATING
			WHERE  RATING.Fountain=%d
		""" % (row['ID']))[0]['Rating']
		fountains.append(ftn)

	return render_template('location.html', lat=lat, lon=lon, nearby=fountains)

def format_rating(x):
	if x is None: return 'N/A'
	return x

@app.route('/fountain/<id>')
def display_fountain(id):
	ftn_info = execute_query("""
		SELECT Lat, Lon
		FROM   FOUNTAIN
		WHERE  ID=%d
		LIMIT  1
	""" % int(id))[0]

	lat=ftn_info['Lat']
	lon=ftn_info['Lon']

	ratings = execute_query("""
		SELECT AVG(Overall)     AS Overall,
		       AVG(Pressure)    AS Pressure,
		       AVG(Temperature) AS Temperature,
		       AVG(Taste)       AS Taste,
		       COUNT(*)         AS Count
		FROM   RATING
		WHERE  Fountain=%d
	""" % int(id))[0]

	overall=ratings['Overall']
	pressure=ratings['Pressure']
	temperature=ratings['Temperature']
	taste=ratings['Taste']
	num_ratings=ratings['Count']

	return render_template('display_fountain.html', id=id, lat=lat, lon=lon, num_ratings=num_ratings,
		overall    =format_rating(overall),
		pressure   =format_rating(pressure),
		temperature=format_rating(temperature),
		taste      =format_rating(taste))



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
