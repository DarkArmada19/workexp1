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
        return render_template('homepage.html')

@app.route('/homepage', methods=['POST'])
def homepage():
    username = str(request.form['username'])
    password = str(request.form['password'])
    

    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()

    query = ("SELECT ID, user_login, user_pass, user_firstname, user_lastname, user_gender FROM fb_userlogin WHERE user_pass = \'" + password + "\' AND user_login = \'" + username + "\'")

    cursor.execute(query)   
    
    for (row) in cursor:
        session["user_id"]=row[0]
        print(session.get("user_id"))
        session["user_login"]=row[1]
        print(session.get("user_login"))
        session["user_pass"]=row[2]
        print(session.get("user_pass"))
        session["user_firstname"]=row[3]
        print(session.get("user_firstname"))
        session["user_lastname"]=row[4]
        print(session.get("user_lastname"))
        session["user_gender"]=row[5]

    cursor.close()
    cnx.close()
    return render_template('homepage.html')

@app.route('/trans_transfer', methods=['POST','GET'])
def trans_transfer():
# Read username and password from form parameters.
    user_id = session.get('user_id')
    print(user_id)
    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()

    query = ("SELECT Transac_ID, Transac_amount, Transac_date, Transac_desc, Transac_posneg FROM fb_transactions WHERE Transac_UID = \'" + str(user_id) + "\'")

    cursor.execute(query) 

    rows=cursor.fetchall()
    cursor.close()
    cnx.close()

    print(rows)

    return render_template('transactions.html', transactions=rows)

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
    gender = request.form.get('gender')
    print(int(gender))
    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()
    sql = "INSERT INTO fb_userlogin (user_login, user_pass, user_email, user_firstname, user_lastname, user_gender) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, password, email, firstname, lastname, gender)
    cursor.execute(sql, val)
    cnx.commit()

    for (row) in cursor:
        session["user_login"]=row[0]
        session["user_pass"]=row[1]
        session["user_email"]=row[2]
        session["user_firstname"]=row[3]
        session["user_lastname"]=row[4]
        session["user_gender"]=row[5]

    cursor.close()
    cnx.close()
    print (gender)
    return render_template('homepage.html')

@app.route("/money")
def money():
    return render_template("money.html")

@app.route("/submitm")
def submitm():
    Transac_UID = session.get('user_id')
    Transac_amount = str(request.form['Transac_amount'])
    print(Transac_amount)
    Transac_desc = str(request.form['Transac_desc'])
    print(Transac_desc)
    Transac_posneg = request.form.get('Transac_posneg')
    print(Transac_posneg)
    cnx = mysql.connector.connect(user='root', database='fakebank')
    cursor = cnx.cursor()
    sql = "INSERT INTO fb_transactions (Transac_UID, Transac_amount, Transac_desc, Transac_posneg) VALUES (%s, %s, %s, %s)"
    val = (Transac_UID, Transac_amount, Transac_desc, Transac_posneg)
    cursor.execute(sql, val)
    cnx.commit()

    for (row) in cursor:
        session["Transac_UID"]=row[0]
        session["Transac_amount"]=row[1]
        session["Transac_date"]=row[2]
        session["Transac_desc"]=row[3]
        session["Transac_posneg"]=row[4]

    cursor.close()
    cnx.close()
    print (Transac_posneg)
    return redner_template("trnasactions.html")
    

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