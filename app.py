# -*- coding: utf-8 -*-

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
app.config['UPLOADS'] = 'static/images/'
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 # 5 MB


app.secret_key = 'able baker charlie'

<<<<<<< HEAD
DB = 'alee31_db' #CHANGE
=======
DB = 'feed2019_db' #CHANGE
>>>>>>> d256323ba5f96b86f4456b6c45010d10d85879c6

@app.route('/')
def index():
    if "username" in session:
       return redirect(url_for("home"))
    return render_template('signup.html', page_title='Feed')

DSN = None

def getConn():
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    return dbi.connect(DSN)


# display all posts
# change to only following posts later or maybe another route for follwing posts
@app.route("/home/") 
def home():
    conn = db.getConn(DB)
    posts = db.getAllPosts(conn)
    #print(posts)
    print(session["username"])
    if "username" not in session:
        flash("Please log in or sign up to continue")
        return redirect(url_for("index"))
    username = session['username']
    # how should they be sorted -- bootstrap card thing inserts by column and not row
    
    return render_template("home.html", page_title="Home • Feed", posts=posts, username = username)

# for now return all results where post name, tag, restaurant match
@app.route("/search/", methods=["GET"])
def search():
    query = request.values.get('query')
    type_ = request.values.get('type')
    conn = db.getConn(DB)

    if type_ == 'posts':
        posts = db.getQueryPosts(conn, query)
        if not posts:
            flash ("no posts found")
        return render_template("home.html", page_title = "Results", posts=posts)
   
    else:
        users = db.getQueryUsers(conn, query)
        if not users:
            flash("no users found")
        return render_template("home.html", page_title="Results", users=users)

# individual post
@app.route('/post/<pid>/')
def post(pid):
    # can people see posts without logging in -- for now, don't need to be logged in
    user = None
    if "username" in session:
        user = session['username']
    
    conn = db.getConn(DB)
    post = db.getSinglePost(conn, pid)
    tags = db.getTagsofPost(conn, pid)
    if not user or user != post['username']:
        posted = False
    else:
        posted = True
    print(posted)
    if not post:
        flash("Post not found")
    return render_template("post.html", post=post, tags=tags, posted=posted)

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

            os.mkdir('static/img/{}'.format(uid)) 
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
            #print(profPic['profpicPath'])
            #session['visits'] = 1+int(session['visits'])
            return redirect(url_for('home'))
            #return redirect(url_for('profile', username= username))
            #return render_template('profile.html', profName=username, uid=uid, fname = fullName, bio = bioText['biotxt'], ppic = profPic['profpicPath']) #THIS WORKS
        

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

@app.route('/upload/', methods=["GET", "POST"])
def upload():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('upload.html')
        if request.method == 'POST':
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
                #what gets put into the database
                filePath = os.path.join('images/{}/'.format(uid), filename)
                conn = getConn()
                curs = dbi.cursor(conn)
                curs.execute(
                    '''insert into Posts(uid,pname,rating,price,review,restaurant,location, imgPath, time) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s, now())''',
                    [uid, name, rating, price, review, restaurant, location, filePath])
                flash('Upload successful')
                return render_template('upload.html')
            except Exception as err:
                print("upload failed because " + str(err))
                flash('Upload failed {why}'.format(why=err))
                return render_template('upload.html')
    else:
            flash('You are not logged in. Please login or join')
            return redirect( url_for('index') )

# i think we can combine the 2 profiles
@app.route('/profile/')
def redirProfile():
    username = session['username']
    return redirect(url_for('profile', username = username))


@app.route('/profile/<username>')
def profile(username): 
    conn = getConn()
    print(username)
    #  username = session['username']
    try:
        uid = db.getUid(conn, username)
        print(uid)

        if not uid:

            print("here")
            flash("User not found")
            return render_template("home.html")

        uid=uid['uid']
        fullName = db.getFullName(conn, uid)
        bioText = db.getBioText(conn, uid)
        profPic = db.getPPic(conn, uid)
        posts = db.getPostsByUser(conn, uid)
        #add a way to get fullname and bio text, image file
        return render_template('profile.html', profName=username,
                                    uid=uid, fname = fullName['fullname'], bio = bioText['biotxt'], ppic = profPic['profpicPath'] 
                                    ,posts = posts)
    except Exception as err:
        flash("user not found")
        return redirect(request.referrer)
     
@app.route('/editprofile/', methods= ["POST"])
def editProf():
    uid = session['uid']
    username = session['username']
    conn = getConn()

    #upload folder path, and allowed extension of file images
    UPLOAD_FOLDER = 'static/img/{}/'.format(uid)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

    #check allowed files 
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    #if 'file' not in request.files: ADD LATER WHERE PEOPLE CAN SPECIFY WHAT INPUT FIELDS THEY WOULD LIKE TO UPDATE, NOT REQUIRED TO UPDATE ALL OF THE FIELDS
            #flash('No file part')
            #return redirect('')
        
    file = request.files['pic']
    filePath = None
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #get the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #save the file to the upload folder destination
            filePath = os.path.join('img/{}/'.format(uid), filename) #make a modified path so the profile.html can read it
            #print("filePath " + filePath)
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
    else:
        flash('not valid file type') #flash a message for errors of file uploads
        return redirect(url_for('profile', username = username))
    
    #requests from the form
    fullName = request.form['fName']
    biotext = request.form['bioText']
    db.updateProfile(conn, uid, fullName, biotext, filePath) #update profile

    return redirect(url_for('profile', username = username))

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