
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory)
from werkzeug import secure_filename

app = Flask(__name__)

import os
import dbi
import bcrypt
import db # database stuff

app.secret_key = 'able baker charlie'

DB = 'rnavarr2_db' #CHANGE

@app.route('/')
def index():
    return render_template('signup.html', page_title='Feed')

DSN = None

def getConn():
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    return dbi.connect(DSN)

# display all posts
# change to only following posts later or maybe another route for follwing posts
@app.route("/home/") # users don't have to be logged in right to see home feed right?
def home():
    print("clicked home")
    
    conn = db.getConn(DB)
    posts = db.getAllPosts(conn)

    # how should they be sorted -- bootstrap card thing inserts by column and not row


    return render_template("home.html", page_title="Home", posts=posts)

# for now return all results where post name, tag, restaurant match
@app.route("/search/", methods=["POST"])
def search():
    query = request.values.get('query')
    print(query)
    conn = db.getConn(DB)
    posts = db.getQueryAll(conn, query)

    print(posts)

    # if no posts flash


    return render_template("home.html", page_title = "Search Results", posts=posts)

@app.route('/signUp/', methods=["GET","POST"])
def signUp():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        try:
            fullname = request.form['fName'] 
            email = request.form['email']
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            profpicPath = 'img/default_profilepic.jpeg'
            if passwd1 != passwd2:
                flash('passwords do not match')
                return redirect( url_for('index'))
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            #print(passwd1, type(passwd1), hashed, hashed_str)
            conn = getConn()
            curs = dbi.cursor(conn)
            try:
                curs.execute('''INSERT INTO Users(uid,fullname,email,username,hashed, biotxt, profpicPath)
                                VALUES(null,%s,%s,%s,%s, null, %s)''',
                            [fullname, email, username, hashed_str, profpicPath])
            except Exception as err:
                flash('That username is taken: {}'.format(repr(err)))
                return redirect(url_for('index'))
            curs.execute('select last_insert_id()')
            row = curs.fetchone()
            uid = row[0]
            #flash('FYI, you were issued UID {}'.format(uid))
            session['username'] = username
            session['uid'] = uid
            session['logged_in'] = True
            session['fullname'] = fullname
            #session['visits'] = 1
            return redirect(url_for('user', username=username) )
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
            curs.execute('''SELECT *
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
            #print('hashed: {} {}'.format(hashed,type(hashed)))
            # print('passwd: {}'.format(passwd))
            #print('hashed.encode: {}'.format(hashed.encode('utf-8')))
            bc = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            #print('bcrypt: {}'.format(bc))
            #print('str(bcrypt): {}'.format(str(bc)))
            #print('bc.decode: {}'.format(bc.decode('utf-8')))
            #print('equal? {}'.format(hashed==bc.decode('utf-8')))
            hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == hashed:
                #flash('successfully logged in as '+username)
                session['username'] = username
                session['uid'] = row['uid']
                session['logged_in'] = True
                session['fullname'] = row['fullname'] #add other stuff in the table so the profile.html can get this stuff
                
                #session['visits'] = 1
                return redirect(url_for('user', username=username) ) #add full name, biotext...etc so user() can get them
            else:
                flash('login incorrect. Try again or join')
                return redirect( url_for('index'))
        except Exception as err:
            flash('form submission error '+str(err))
            return redirect( url_for('index') )


@app.route('/user/<username>')
def user(username):
    try:
        # don't trust the URL; it's only there for decoration
        conn = getConn()
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            fullName = session['fullname']
            #session['visits'] = 1+int(session['visits'])
            bioText = db.getBioText(conn, uid)
            profPic = db.getPPic(conn, uid)
            print(profPic['profpicPath'])
            os.mkdir('img/{}'.format(uid)) #this doesn't work, fix how to make directories using OS
            #session['visits'] = 1+int(session['visits'])
            return render_template('profile.html', 
                                   profName=username,
                                   uid=uid, fname = fullName, bio = bioText['biotxt'], ppic = profPic['profpicPath'] 
                                   ) #make sure to add the otherstuff so profile.html knows
        #visits=session['visits'], #page_title='My App: Welcome {}'.format(username)

        else:
            flash('You are not logged in. Please login or join')
            return redirect(url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect(url_for('index') )

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







@app.route('/profile/<username>')
def profile():
     username = session['username']
     uid = session['uid']
     #add a way to get fullname and bio text, image file
     return render_template('profile.html',name=username, uid=uid)
     
@app.route('/editprofile/', methods= ["POST"])
def editProf():
    uid = session['uid']
    
    UPLOAD_FOLDER = 'img/{}'.format(uid)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    conn = getConn()
    #if 'file' not in request.files:
            #flash('No file part')
            #return redirect('')
    file = request.files['pic']
    filePath = None
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
    else:
        flash('not valid file type')
        # redirect to profile() function
    uid = session['uid']
    username = session['username']
    fullName = request.form['fName']
    #image = request.form['pic']
    #print(image)
    biotext = request.form['bioText']
    db.updateProfile(conn, uid, fullName, biotext)
    bioText = db.getBioText(conn, uid)
    
    profPic = db.getPPic(conn, uid)
    
    #add upload pic option
    return render_template('profile.html', 
                                   profName=username,
                                   uid=uid, fname = fullName, bio = bioText['biotxt'], ppic = filename)

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