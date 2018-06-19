from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
import mysql.connector

app = Flask(__name__)
user = 'root'
database = 'fakebank'

@app.route('/')
def home():
    if not session.get('user_id'):
        return render_template('loginuser.html')
    else:
        return "Hello",name
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    
    username = str(request.form['username'])
    password = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]) )
    result = query.first()

    if password == 'JohnMan' and  username == 'manpassword':
        print('Hey, John!')
        session['user_id'] = True
        print(session.get('user_id'))
    else:
        flash('Wrong password!')
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='localhost', port=5000)