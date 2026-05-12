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



@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
	if request.method == 'POST':
		try:
			# Extract form data
			username = request.form['username']

			# First check: is username valid?
			if not validate_username(username):
				raise Exception('Username is invalid.')
			
			# Second check: does the username already exist?
			user_row = execute_query("""
				SELECT *
				FROM   CREATORS
				WHERE  Name='%s'
			""" % username)
			
			if (len(user_row) != 0):
				raise Exception('A user by that name already exists.')
			
			# Allocate a new user ID. TODO: do this more smartly.
			max_id_row = execute_query("""
				SELECT MAX(ID) AS ID
				FROM   CREATORS
			""")
			new_id = max_id_row[0]['ID'] + 1

			# Finally, add a user to the database.
			
			execute_update_query("""
				INSERT INTO CREATORS VALUES (%d, '%s')
			""" % (new_id, username))
			
			flash('User added successfully.', 'success')
		except Exception as e:
			# An error occurred.
			flash('An error occurred: %s' % str(e), 'error')
		
		# Redirect to home page
		return redirect(url_for('home'))
	else:
		# Render the form page if the request method is GET
		return render_template('add_user.html')



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


@app.route('/user/<userid>')
def display_user(userid):
	try:
		# Query the database
		user_row = execute_query("""
			SELECT CREATORS.Name AS Name
			FROM   CREATORS
			WHERE  CREATORS.ID=%d
			LIMIT  1
		""" % int(userid))

		# Get hacks
		hacks = execute_query("""
			SELECT HACK.ID AS ID, HACK.Title AS Title, HACK.Type AS Type
			FROM   HACK, HACK_AUTHOR
			WHERE  HACK_AUTHOR.UserID=%d AND HACK_AUTHOR.HackID=HACK.ID
		""" % int(userid))
		
		username = user_row[0]['Name']
		return render_template('display_user.html', username=username, hacks=hacks)
	except:
		# Error display (db error, no user, bad user ID)
		return render_template('display_user_error.html')



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
