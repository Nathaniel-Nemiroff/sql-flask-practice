from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

app=Flask(__name__)
app.secret_key='FFORIMENNAHTAN'

mysql = MySQLConnector(app, 'registerdb')#change database for appropriate functionality

#print mysql.query_db("SELECT name FROM countries")

#session['email_msg']=0

@app.route('/')
def index():
	msg=''
	if('regmsg' in session):
		msg=session['regmsg']
		session.pop('regmsg')
	print mysql.query_db("SELECT * FROM users")
	return render_template('index.html',message=msg)

@app.route('/register', methods=['POST'])
def register():
	if request.form:
		first=request.form['first']
		last=request.form['last']
		email=request.form['email']
		pswd=request.form['pswd']
		conf=request.form['conf']

		check=True
		if(len(first)<2 or len(last)<2):
			check=False
			flash('Names must be more than one character long!')
		if(not NAME_REGEX.match(first) or not NAME_REGEX.match(last)):
			check=False
			flash('Name must contain only alphabetic characters!')
		if(not EMAIL_REGEX.match(email)):
			check=False
			flash('Email is not valid!')
		if(len(pswd)<8):
			check=False
			flash('Password must be at least 8 characters!')
		if(not pswd == conf):
			check=False
			flash('Passwords must be the same!')
	
		if(check):
			hashsalt=bcrypt.gensalt()
			hashpass = bcrypt.hashpw(pswd.encode('UTF_8'), hashsalt)
			mysql.query_db("INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES('"+first+"','"+last+"','"+email+"','"+hashpass+"','"+hashsalt+"',NOW(), NOW())")
			session['regmsg']='Registered successfully!'
			return redirect('/')
		else:
			return render_template('register.html')
	else:
		return render_template('register.html')



@app.route('/login', methods=['POST'])
def login():
	if request.form:

		passchk = mysql.query_db("SELECT * FROM users WHERE email = '"+request.form['email']+"'")
		print 'debug'
		print passchk
		print 'debug'
		if not passchk:
			flash('Username or password incorrect!')
			return render_template('login.html')
		hashch = bcrypt.hashpw(request.form['pswd'].encode('UTF_8'),passchk[0]['salt'].encode('UTF_8')) 
		if hashch == passchk[0]['password']:
			session['regmsg']='login successful! Welcome '+passchk[0]['first_name']+' '+passchk[0]['last_name']
			return redirect('/')
		else:
			flash('Username or password incorrect!')
			return render_template('login.html')
	return render_template('login.html')


'''
	if not 'email_msg' in session:
		session['email_msg']=0
	message=''
	emails=''
	if session['email_msg']>0:
		emails=mysql.query_db("SELECT * FROM emails")
		message='Email is valid!'
		session['email_msg']=0
	elif session['email_msg']<0:
		message='Email is not valid!'
		session['email_msg']=0
	return render_template('index.html',msg=message,all_emails=emails)

@app.route('/emails', methods=['POST'])
def pushemail():
	email=request.form['email']

	if EMAIL_REGEX.match(email):
		mysql.query_db("INSERT INTO emails (email, created_at, updated_at) VALUES('"+email+"',NOW(), NOW())")
		session['email_msg']=1
	else:
		session['email_msg']=-1
	return redirect('/')
'''

'''
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
'''



app.run(debug=True)
