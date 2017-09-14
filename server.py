from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
from datetime import datetime, date, time

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = 'ThisIsEmailValidation'
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addemail', methods=['POST'])
def create():
    if len(request.form['email']) == 0:
        flash('Email cannot be blank', 'error')
        return redirect('/')
    elif not emailRegex.match(request.form['email']):
        flash('Email is not valid!', 'error')
        return redirect('/')
    else:
        insert = "INSERT INTO myfriends (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        
        data = {
                'email': request.form['email']
            }
        mysql.query_db(insert, data)
        flash('The email address you entered (___) is a VALID email address! Thank you!', 'success')
        emails = mysql.query_db("SELECT myfriends.email, myfriends.created_at FROM myfriends")
        #return redirect('/')
        return render_template('success.html', emails=emails)

@app.route('/reset', methods=['POST'])
def delete():
    query = "DELETE FROM myfriends"
    mysql.query_db(query)
    return redirect('/')

app.run(debug=True)