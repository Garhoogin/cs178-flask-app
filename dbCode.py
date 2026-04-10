# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
	"""Executes a SELECT query and returns all rows as dictionaries."""
	con = get_conn()
	cur = con.cursor(pymysql.cursors.DictCursor)
	cur.execute(query, args)
	con.commit()
	rows = cur.fetchall()
	cur.close()
	return rows

def execute_update_query(query, args=()):
	# Runs a query to update the database.
	con = get_conn()
	cur = con.cursor(pymysql.cursors.DictCursor)
	cur.execute(query, args)
	con.commit()
	cur.close()
