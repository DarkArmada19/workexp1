from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
import mysql.connector

app = Flask(__name__)
@app.route('/')
def home():
    if not session.get('user_id'):
        return render_template('homepage.html')
    else:
        return render_template('user.html')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

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

    
    
    
    #     if username == user_login and password == user_pass:
    #         print('Hey, dude!')
    #         session['user_id'] = True
    #         print(session.get('user_id'))
    #         cnx = mysql.connector.connect(user='root', database='fakebank')
    #         cursor = cnx.cursor()
    #         print(username)
    #         print(password)
    #         query = ("SELECT ID FROM fb_userlogin WHERE user_login = 'JohnMan'")
    #         cursor.execute(query)
    #         for (ID) in cursor:
    #             print("{}").format(ID)
    #             print(user_id)
    #     else:
    #         return render_template('loginuser.html')
    #     return home()
 
    cursor.close()
    cnx.close()
    return render_template('user.html', userid=session.get("user_id"), name=session.get("user_1name") )


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
    success = (cursor.rowsaffected != 0)
    #cnx.commit()
    #print(cursor.rowsaffected, "record inserted.")
    cursor.close()
    cnx.close()
    if success == True:
        createsuccess()
    else:
        error()

@app.route("/createsuccess")
def createsuccess():
    return render_template('createsuccess.html')

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