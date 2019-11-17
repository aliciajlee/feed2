from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory)
from werkzeug import secure_filename

app = Flask(__name__)

import os
import dbi
import bcrypt
import db

app.secret_key = 'able baker charlie'

def getConn():
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    return dbi.connect(DSN)

@app.route('/')
def index():
    return render_template('main.html', page_title='Feed')

# display all posts
# change to only following posts later or maybe another route for follwing posts
@app.route("/home/") # users don't have to be logged in right to see home feed right?
def home():

    

    return render_template("home.html", page_title="Home")

#search by dish name, tag, restaurant, etc
@app.route("/search/<query>", methods=["POST"])
def search(query):
    pass



@app.route('/signUp/', methods=["GET","POST"])
def signUp():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        try:
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            # ADD USERNAME STUFF   
            if passwd1 != passwd2:
                flash('passwords do not match')
                return redirect( url_for('index'))
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            print(passwd1, type(passwd1), hashed, hashed_str)
            conn = db.getConn()
            curs = dbi.cursor(conn)
            try:
                curs.execute('''INSERT INTO Users(uid,username,hashed)
                                VALUES(null,%s,%s)''',
                            [username, hashed_str])
            except Exception as err:
                flash('That username is taken: {}'.format(repr(err)))
                return redirect(url_for('index'))
            curs.execute('select last_insert_id()')
            row = curs.fetchone()
            uid = row[0]
            flash('FYI, you were issued UID {}'.format(uid))
            session['username'] = username
            session['uid'] = uid
            session['logged_in'] = True
            session['visits'] = 1
            return redirect( url_for('user', username=username) )
        except Exception as err:
            flash('form submission error '+str(err))
            return redirect( url_for('index') )
        
@app.route('/login/', methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try:
            username = request.form['username']
            passwd = request.form['password']
            conn = getConn()
            curs = dbi.dictCursor(conn)
            curs.execute('''SELECT uid,hashed
                        FROM Users
                        WHERE username = %s''',
                        [username])
            row = curs.fetchone()
            if row is None:
                # Same response as wrong password,
                # so no information about what went wrong
                flash('login incorrect. Try again or join')
                return redirect( url_for('index'))
            hashed = row['hashed']
            print('hashed: {} {}'.format(hashed,type(hashed)))
            print('passwd: {}'.format(passwd))
            print('hashed.encode: {}'.format(hashed.encode('utf-8')))
            bc = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            print('bcrypt: {}'.format(bc))
            print('str(bcrypt): {}'.format(str(bc)))
            print('bc.decode: {}'.format(bc.decode('utf-8')))
            print('equal? {}'.format(hashed==bc.decode('utf-8')))
            hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == hashed:
                flash('successfully logged in as '+username)
                session['username'] = username
                session['uid'] = row['uid']
                session['logged_in'] = True
                session['visits'] = 1
                # return redirect( url_for('user', username=username) )  why user
                return redirect(url_for('home'))
            else:
                flash('login incorrect. Try again or join')
                return redirect( url_for('index')) # should go back to login page?
        except Exception as err:
            flash('form submission error '+str(err))
            return redirect( url_for('index') )


@app.route('/user/<username>')
def user(username):
    try:
        # don't trust the URL; it's only there for decoration
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            session['visits'] = 1+int(session['visits'])
            return render_template('greet.html',
                                   page_title='My App: Welcome {}'.format(username),
                                   name=username,
                                   uid=uid,
                                   visits=session['visits'])

        else:
            flash('You are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

@app.route('/logout/')
def logout():
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('uid')
            session.pop('logged_in')
            flash('You are logged out')
            return redirect(url_for('index'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )


if __name__ == '__main__':
    import sys,os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
