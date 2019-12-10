# -*- coding: utf-8 -*-
# test

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, Response)
from werkzeug import secure_filename

app = Flask(__name__)

import os
import dbi
import imghdr
import bcrypt
import db # database stuff
import json

# for file uploads
app.config['UPLOADS'] = 'static/images/'
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 # 5 MB


app.secret_key = 'able baker charlie'

DB = 'feed2019_db' #CHANGE

@app.route('/')
def index():
    if "username" in session:
       return redirect(url_for("home"))
    return render_template('signup.html', page_title='Feed')

DSN = None

# we should move this to db
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
    if "username" not in session:
        flash("Please log in or sign up to continue")
        return redirect(url_for("index"))
    username = session['username']
    # how should they be sorted -- bootstrap card thing inserts by column and not row
    return render_template("home.html", page_title="Home • Feed", posts=posts, username=username,
                            options=True)


# for now return all results where post name, tag, restaurant, username, fullname match
@app.route("/search/", methods=["GET"])
def search():
    query = request.values.get('query')
    type_ = request.values.get('type')
    conn = db.getConn(DB)
    if type_ == 'posts':
        posts = db.getQueryPosts(conn, query)
        if not posts:
            flash ("no posts found")
        flash("Post results for '{}'".format(query))
        return render_template("home.html", page_title="Results", posts=posts, options=True)
    else:
        # might be nice to have a separate html for users
        users = db.getQueryUsers(conn, query)
        if not users:
            flash("no users found")
        flash("User results for '{}'".format(query))
        return render_template("home.html", page_title="Results",users=users, options=False)


# display info of an individual post
@app.route('/post/<pid>/')
def post(pid):
    # can people see posts without logging in -- for now, don't need to be logged in
    conn = db.getConn(DB)
    post = db.getSinglePost(conn, pid)
    if not post:
        flash("Post not found")
        return redirect(request.referrer)

    tags = db.getTagsofPost(conn, pid)

    rating = post['rating']

    user = None if 'username' not in session else session['username']
    posted = user == post['username']
    
    all_tags = []
    if posted:
        all_tags = db.getAllTags(db.getConn(DB)) # for displaying tags in edit post

    return render_template("post.html", post=post, pid=pid, tags=tags, posted=posted, all_tags=all_tags)


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
    if "username" in session:
        return redirect(url_for("home"))
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
            postconn = db.getConn(DB)
            tags = db.getAllTags(postconn)
            return render_template('upload.html', tags = tags)
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
                tags = request.form.getlist("tags")
                f = request.files['pic']

                #make sure image is not too big
                fsize = os.fstat(f.stream.fileno()).st_size
                if fsize > app.config['MAX_CONTENT_LENGTH']:
                    raise Exception('File is too big')
                
                #make sure image is right type
                mime_type = imghdr.what(f)
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
                
                #the filepath that gets put into the database
                filePath = os.path.join('images/{}/'.format(uid), filename)

                #add to post table
                conn = getConn()
                curs = dbi.cursor(conn)
                curs.execute(
                    '''insert into Posts(uid,pname,rating,price,review,restaurant,location, imgPath, time) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s, now())''',
                    [uid, name, rating, price, review, restaurant, location, filePath])
                
                #add to Tagpost table
                for tag in tags:
                    curs.execute('''insert into Tagpost(pid,tid) values (%s,%s)''', [pid, tag])
                
                flash('Upload successful')
                return redirect(url_for("index"))
            
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
    try:
        uid = db.getUid(conn, username)
        print(uid)
        if not uid:
            flash("User not found")
            return render_template("home.html")
        uid=uid['uid']
        fullName = db.getFullName(conn, uid)
        bioText = db.getBioText(conn, uid)
        profPic = db.getPPic(conn, uid)
        posts = db.getPostsByUser(conn, uid)
        #add a way to get fullname and bio text, image file
        return render_template('profile.html', profName=username,
                                    uid=uid, fname = fullName['fullname'], bio = bioText['biotxt'], 
                                    ppic = profPic['profpicPath'], posts = posts)
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


@app.route('/delete_post/<pid>', methods=['POST'])
def delete_post(pid):
    # might be good to check that user deleting post is valid
    # if 
    #     flash("post doesn't belong to user logged in")
    try:
        conn = db.getConn(DB)
        db.deletePost(conn, pid)
    except Exception as err:
        flash("error deleting post")
        print("error deleting post")
        return redirect(request.referrer)

    flash("Successfully deleted post")
    return redirect(url_for("home"))

# edit a post's name, resturant, location, rating, price, review
@app.route('/edit_post/<pid>', methods=['POST'])

# @Scott--can we pass variables from jinja to python function?
# trying to pass tags of a post that we got when we rendered post.html
def edit_post(pid, old_tags=None): 
    
    # conn = db.getConn(DB)

    pname = request.form.get("pname")
    restaurant = request.form.get("restaurant")
    location = request.form.get("location")
    rating = request.form.get("rating")
    price = request.form.get("price")
    review = request.form.get("review")
    new_tags = request.form.getlist("tags")
 
    # print("delete " + delete)
    # print("insert " + insert)

    try:
        db.editPost(db.getConn(DB), pid, pname, restaurant, location, rating, price, review)

        # @Scott is it better to delete all tags of a Post and then add all new tags we get in the form,
        # or find the new tags that should be added and the old tags that should be deleted
        # and insert/delete them?
        db.deleteAllTagsofPost(db.getConn(DB), pid)

        for tid in new_tags:
            db.insertTagPost(db.getConn(DB), pid, tid)

    except Exception as err:
        print("error editing post")
        flash("error editing post")
        return redirect(request.referrer)

    flash("Sucessfully edited post")
    return redirect(request.referrer)

@app.route('/tags/<tag>/', methods=["GET"])
def show_tag_posts(tag):
    conn = db.getConn(DB)
    #convert from tag to tid
    tid = db.getTid(conn,tag)['tid']
    #get posts with the tag
    posts = db.getPostsWithTid(conn, tid)
    #check if user is logged in
    if "username" not in session:
        flash("Please log in or sign up to continue")
        return redirect(url_for("index"))
    username = session['username']
    title = "posts under " + tag
    return render_template("home.html", page_title= title, posts=posts, username=username,
                            options=True)

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