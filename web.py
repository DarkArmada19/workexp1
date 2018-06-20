from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('user_id'):
        return render_template('loginuser.html')
    else:
        return render_template('homepage.html')

@app.route('/homepage', methods=['POST'])
def homepage():
    username = str(request.form['username'])
    password = str(request.form['password'])

    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()

    query = ("SELECT ID, user_login, user_firstname FROM fb_userlogin WHERE user_login = \'" + username + "\'")

    cursor.execute(query)   
    
    for (row) in cursor:
        session["user_id"]=row[0]
        print(session.get("user_id"))
        session["user_logname"]=row[1]
        print(session.get("user_logname"))
        session["user_1name"]=row[2]
        print(session.get("user_1name"))
 
    cursor.close()
    cnx.close()
    return render_template('homepage.html', userid=session.get("user_id"), name=session.get("user_1name"))

@app.route('/login', methods=['POST'])
def do_admin_login():
# Read username and password from form parameters.
    username = str(request.form['username'])
    password = str(request.form['password'])

    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()

    query = ("SELECT ID, user_login, user_firstname FROM fb_userlogin WHERE user_login = \'" + username + "\'")

    cursor.execute(query)   
    
    for (row) in cursor:
        session["user_id"]=row[0]
        print(session.get("user_id"))
        session["user_logname"]=row[1]
        print(session.get("user_logname"))
        session["user_1name"]=row[2]
        print(session.get("user_1name"))
 
    cursor.close()
    cnx.close()
    return render_template('user.html', userid=session.get("user_id"), name=session.get("user_1name") )

@app.route('/transactions', methods=['POST'])
if session.get('user_id'):
    return render_template('transactions.html')
else:
def transactions():
# Read username and password from form parameters.
    username = str(request.form['username'])
    password = str(request.form['password'])
    IDreal = str(request.form['IDreal'])

    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()

    query = ("SELECT User_ID, Transac_amount, Transac_date, Transac_details, pos_or_neg FROM fb_transactions WHERE User_ID = \'" + IDreal + "\'")

    cursor.execute(query)   
    
    for (row) in cursor:
        session["user_id"]=row[0]
        print(session.get("user_id"))
        session["user_amt"]=row[1]
        print(session.get("user_amt"))
        session["user_date"]=row[2]
        print(session.get("user_date"))
        session["user_desc"]=row[3]
        print(session.get("user_desc"))
        session["user_posneg"]=row[4]
        print(session.get("user_posneg"))
 
    cursor.close()
    cnx.close()
    return render_template('transactions.html', userida=session.get("user_id"), amt=session.get("user_amt"), date=session.get("user_date"), desc=session.get("user_desc"), posneg=session.get("user_posneg"))

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/createuser", methods=['POST'])
def createuser():
    username = str(request.form['username'])
    password = str(request.form['password'])
    email = str(request.form['email'])
    firstname = str(request.form['firstname'])
    lastname = str(request.form['lastname'])
   
    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()
    sql = "INSERT INTO fb_userlogin (user_login, user_pass, user_email, user_firstname, user_lastname) VALUES (%s, %s, %s, %s, %s)"
    val = (username, password, email, firstname, lastname)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('success.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/error")
def error():
    return render_template('error.html')


@app.route("/logout")
def logout():
    session['user_id'] = False
    return render_template('homepage.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='localhost', port=5000)