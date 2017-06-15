from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app=Flask(__name__)

mysql = MySQLConnector(app, 'friendsdb1')

#print mysql.query_db("SELECT name FROM countries")


@app.route('/')
def index():
	print 'AT INDEX-----------------------------'
	friends = mysql.query_db("SELECT * FROM friends")
	print friends
	#print 'test-----------------------------'
	#print mysql.query_db("SELECT first_name FROM friends")
	#print 'test-----------------------------'
	
	return render_template('index.html', all_friends=friends)

@app.route('/friends',methods=['POST'])
def create():
	# ......
	mysql.query_db("INSERT INTO friends (name, age, friend_since)VALUES('"+request.form['name']+"', '"+request.form['age']+"', NOW());")
	return redirect('/')


app.run(debug=True)
