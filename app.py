from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, Response)
from werkzeug import secure_filename
app = Flask(__name__)

import os
import dbi
import imghdr
import bcrypt
import db # database stuff

# for file uploads
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 # 5 MB


app.secret_key = 'able baker charlie'

DB = 'alee31_db' #CHANGE

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
    
    if not session.get("logged_in"):
        flash("Please log in to continue")
        return redirect(url_for("login"))
    conn = db.getConn(DB)
    posts = db.getAllPosts(conn)

    # how should they be sorted -- bootstrap card thing inserts by column and not row


    return render_template("home.html", page_title="Home • Feed", posts=posts)

# for now return all results where post name, tag, restaurant match
@app.route("/search/", methods=["GET"])
def search():
    query = request.values.get('query')
    print(query)
    conn = db.getConn(DB)
    posts = db.getQueryPosts(conn, query)

    print(posts)

    # if no posts flash


    return render_template("home.html", page_title = "Results • Feed", posts=posts)

@app.route('/signUp/', methods=["GET","POST"])
def signUp():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        try:
            email = request.form['email']
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            if passwd1 != passwd2:
                flash('passwords do not match')
                return redirect( url_for('index'))
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            print(passwd1, type(passwd1), hashed, hashed_str)
            conn = getConn()
            curs = dbi.cursor(conn)
            try:
                curs.execute('''INSERT INTO Users(uid,username,email,hashed)
                                VALUES(null,%s,%s,%s)''',
                            [username, email, hashed_str])
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
                return redirect( url_for('home') )
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
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            session['visits'] = 1+int(session['visits'])
            return render_template('home.html',
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

@app.route('/upload/', methods=["GET", "POST"])
def upload():
    if 'username' in session:
        if request.method == 'GET':
            print ('in get!')
            return render_template('upload.html')
        if request.method == 'POST':
            print('in post!')
            try:
                uid = session['uid']
                postconn = db.getConn(DB)
                pid = db.getNumPosts(postconn) + 1
                name = request.form['name'] 
                rating = request.form['rating']
                review = request.form['review']
                restaurant = request.form['restaurant']
                location = request.form['location']
                price = request.form['price']
                f = request.files['pic']
                #make sure image is not too big
                fsize = os.fstat(f.stream.fileno()).st_size
                print('file size is {} '.format(fsize))
                if fsize > app.config['MAX_CONTENT_LENGTH']:
                    raise Exception('File is too big')
                #make sure image is right type
                mime_type = imghdr.what(f)
                print('mime type is {}'.format(mime_type))
                if not mime_type or mime_type.lower() not in ['jpeg','gif','png']:
                    raise Exception('Not recognized as JPEG, GIF or PNG: {}'
                                    .format(mime_type))                
                ext = f.filename.split('.')[-1]
                filename = secure_filename('{}.{}'.format(pid,ext))
                user_folder = os.path.join(app.config['UPLOADS'],str(uid))

                #if user folder doesn't exist, create it. Otherwise, upload it
                if not(os.path.isdir(user_folder)):
                    os.mkdir(user_folder)
                pathname = os.path.join(user_folder,filename)
                
                f.save(pathname)
                conn = getConn()
                curs = dbi.cursor(conn)
                curs.execute(
                    '''insert into Posts(uid,pname,rating,price,review,restaurant,location, imgPath, time) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s, now())''',
                    [uid, name, rating, price, review, restaurant, location, filename])
                flash('Upload successful')
                return render_template('upload.html')
            except Exception as err:
                print("upload failed because " + str(err))
                flash('Upload failed {why}'.format(why=err))
                return render_template('upload.html')
    else:
            flash('You are not logged in. Please login or join')
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