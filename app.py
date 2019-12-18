# -*- coding: utf-8 -*-

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, Response, jsonify)
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
DSN = None

# this returns to the home feed if already logged in, otherwise it will direct to signup or login 
@app.route('/')
def index():
    if "username" in session:
       return redirect(url_for("home"))
    return render_template('signup.html', page_title='Feed')


# display all posts
# change to only following posts later or maybe another route for follwing posts
@app.route("/home/") 
def home():
    '''if the user is not loggin, it will flash and redirect to the appropriate page from the index app route. 
    It will get all the posts, keep track of the username, and gets all the tags. Renders the home.html page'''
    conn = db.getConn(DB)
    # posts = db.getAllPosts(conn)
    if "username" not in session:
        flash("Please log in or sign up to continue")
        return redirect(url_for("index"))
    username = session['username']
    tags = db.getAllTags(conn)

    #change this to AJAX later
    tag = request.values.get('tag')
    sort_by = request.values.get("sort-by")
    
    conn.close()

    if(tag):
        return redirect(url_for('show_tag_posts', tag= tag))
    else: 
        conn = db.getConn(DB)
        if not sort_by: 
            sort_by = "recent" # default sort by recent
        if sort_by == "recent":
            posts = db.getAllPosts(conn) # this is close enough to sort by recent
        elif sort_by == "rating":
            posts = db.getAllPostsSortByRating(conn)
        else:
            posts = None
            flash("need to implement sort by price!!!!")
            
        return render_template("home.html", page_title="Home • Feed", posts=posts[::-1], username=username,
                                tags = tags, options=True, sort_by=sort_by)


@app.route('/likes/<post>', methods= ["POST"])   
def likes(post):
    ''' ajax function that updates the number of likes when either a like is added or deleted'''
    try: 
        conn = db.getConn(DB)
        profUID = db.getUid(conn, username)
        numberLikes = db.countLikes(conn, post)
        conn.close()
        return jsonify(numLikes = numberLikes)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )


# eturn all post results where post name, tag, restaurant, username, fullname match
@app.route("/search/", methods=["GET"])
def search():
    '''search by rating or search by time post (most recent) '''
    query = request.values.get('query')
    
    if query and query[-1] == "/":
        query = query[:-1] # bad fix

    type_ = request.values.get('type')
    conn = db.getConn(DB)
    if type_ == "posts/": type_ = "posts" # how to get rid of /?
    if type_ == 'posts': 

        # here we also need to check sorting
        sort_by = request.values.get("sort-by")
        if not sort_by:
            sort_by = "recent"
        if sort_by == "recent":
            posts = db.getQueryPosts(conn, query)
        elif sort_by == "rating":
            posts = db.getQueryPostsSortByRating(conn,query)
        else:
            posts = None
            flash("need to implement sort by price!!!!")
        conn.close()
        if not posts:
            flash ("no posts found")
        flash("Post results for '{}'".format(query))
        return render_template("home.html", page_title="Results", posts=posts[::-1], options=True,
                                    query=query, type=type_, search=True, sort_by=sort_by)
    else:
        # might be nice to have a separate html for users
        users = db.getQueryUsers(conn, query)
        print("type: " + type_)
        conn.close()
        if not users:
            flash("no users found")
        flash("User results for '{}'".format(query))
        return render_template("home.html", page_title="Results",users=users, options=False,
                                    query=query, type=type_)


@app.route('/alike/<post>', methods= ["POST", "GET"])   
def alikes(post):
    '''ajax function to add a like (insert into database). The number of likes is recalculated and sent through jsonify '''
    try: 
        conn = db.getConn(DB)
        db.addLike(conn, post, session['uid'])
        numberLikes = db.countLikes(conn, post)
        conn.close()
        print("here")
        return jsonify(numLikes = numberLikes)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )


@app.route('/dlike/<post>', methods= ["POST", "GET"])   
def dlikes(post):
    ''' ajax function to delete a like (delete into database). The number of likes is recalculated and sent through jsonify'''
    try: 
        conn = db.getConn(DB)
        db.removeLike(conn, post, session['uid'])
        numberLikes = db.countLikes(conn, post)
        conn.close()
        print("number of likes after deleting: " + str(numberLikes))
        return jsonify(numLikes = numberLikes)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )


@app.route('/listofLikes/<post>', methods = ["POST", "GET"])
def likesList(post):
    '''gets the lists of people who liked that particular post '''
    conn = db.getConn(DB)
    #profUID = db.getUid(conn, username)
    pid = post
    userLikesList = db.likesList(conn, pid)
    conn.close()
    return render_template("listofFollowing.html", page_title="Who Likes this post", users = userLikesList, options=False)


''' COMMENTS IMPLEMENTATION WE DID NOT HAVE TIME FOR :(
@app.route('/listofComment/<post>', methods = ["POST", "GET"])
def commentsList(post):
    gets the lists of comments for each post 
    conn = db.getConn(DB)
    comments = db.getComments(conn, pid)
    #profUID = db.getUid(conn, username)
    pid = post
    #return render_template(".html", page_title="Who commented this post", comments = comments)


@app.route('/dcomment/<post>/<comment>', methods= ["POST", "GET"])   
def dcomment(post, comment):
    deletes a comment for each post
    try: 
        conn = db.getConn(DB)
        db.deleteComment(conn, post, session[uid], comment)
        db.getComments(conn, pid)
        return jsonify(comments = comments)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )


@app.route('/acomment/<post>/<comment>', methods= ["POST", "GET"])   
def acomment(post, comment):
  adds a comment for each post 
    try: 
        conn = db.getConn(DB)
        db.addComment(conn, post, session[uid], comment)
        db.getComments(conn, pid)
        return jsonify(comments = comments)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )
'''


# display info of an individual post
@app.route('/post/<pid>/')
def post(pid):
    ''' gets a single post that is rendered on post.html when clicking on the post in the home feed '''
    conn = db.getConn(DB)
    post = db.getSinglePost(conn, pid)
    likes = db.countLikes(conn, pid)

    if not post:
        flash("Post not found")
        return redirect(request.referrer)

    tags = db.getTagsofPost(conn, pid)
    conn.close()

    rating = post['rating']

    user = None if 'username' not in session else session['username']
    posted = user == post['username']
    conn = db.getConn(DB)
    uid = session['uid']
    conn.close()

    conn = db.getConn(DB)
    liked = db.like_trueFalse(conn, pid, uid)
    conn.close()

    all_tags = []
    if posted:
        all_tags = db.getAllTags(db.getConn(DB)) # for displaying tags in edit post

    return render_template("post.html", post=post, pid=pid, tags=tags, posted=posted, 
                            all_tags=all_tags, likes=likes, liked=liked)


@app.route('/signUp/', methods=["GET","POST"])
def signUp():
    ''' gets the info from the sign up form and inserts info into the Users table, otherwise if a field is 
    not filled in, will reupload the page for them to try again '''
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
            conn = db.getConn(DB)
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
            session['username'] = username
            session['uid'] = uid
            session['logged_in'] = True
            session['fullname'] = fullname

            os.mkdir('static/img/{}'.format(uid)) 
            return redirect(url_for('user', username=username) )
        except Exception as err:
            flash('form submission error: field(s) not filled in '+str(err))
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
            conn = db.getConn(DB)
            curs = dbi.dictCursor(conn)
            curs.execute('''SELECT *
                        FROM Users
                        WHERE username = %s''',
                        [username])
            row = curs.fetchone()
            if row is None:
                flash('username and or/password is incorrect. Try again or join') #making it vague like other social media applications for security precautions 
                return redirect( url_for('index'))
            hashed = row['hashed']
            bc = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == hashed:
                session['username'] = username
                session['uid'] = row['uid']
                session['logged_in'] = True
                session['fullname'] = row['fullname'] 
                return redirect(url_for('user', username=username)) 
            else:
                flash('username and or/password incorrect. Try again or join')
                return redirect( url_for('index'))
        except Exception as err:
            flash('please fill in all fields'+str(err))
            return redirect( url_for('index') )


@app.route('/user/<username>')
def user(username):
    ''' gets necessary username information '''
    try:
        conn = db.getConn(DB)
        if 'username' in session:
            username = session['username']
            uid = session['uid']
            fullName = session['fullname']
            bioText = db.getBioText(conn, uid)
            profPic = db.getPPic(conn, uid)
            return redirect(url_for('home'))
        else:
            flash('You are not logged in. Please login or join')
            return redirect(url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect(url_for('index') )


@app.route('/logout/')
def logout():
    '''removes username info from session as user clicks log out and redirects to login/signup page'''
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


@app.route('/upload/', methods=["POST"])
def upload(): 
    '''adds a post's information into the database'''
    name = request.form.get("pname")
    restaurant = request.form.get("restaurant")
    location = request.form.get("location")
    rating = request.form.get("rating")
    price = request.form.get("price")
    review = request.form.get("review")
    tags = request.form.getlist("tags")

    uid = session['uid']
    postconn = db.getConn(DB)
    try:
        #add everything but the imgpath to the Post table
        pid = db.insertPost(postconn, uid, name, rating, price, review, restaurant, location)
        f = request.files["upload"]

        ext = f.filename.split('.')[-1]
        filename = secure_filename('{}.{}'.format(pid,ext))
        user_folder = os.path.join(app.config['UPLOADS'],str(uid))

    
        #if user folder doesn't exist, create it. Otherwise, upload it
        if not(os.path.isdir(user_folder)):
            os.mkdir(user_folder)
        pathname = os.path.join(user_folder,filename)
        f.save(pathname)
        
        #add the renamed imgpath into the Post table
        filePath = os.path.join('images/{}/'.format(uid), filename)

        db.insertFilepath(postconn, filePath, pid)

        #add to Tagpost table
        for tag in tags:
            tid = db.getTid(postconn, tag)
            db.insertTagPost(postconn,pid,tid)
        flash('Upload successful')
        return redirect(url_for('index'))

    except Exception as err:
        print("upload failed because " + str(err))
        flash('Upload failed {why}'.format(why=err))
        return redirect( url_for('index') )


@app.route('/profile/')
def redirProfile():
    ''' way to solve jinja issue where I needed the session's username'''
    username = session['username']
    return redirect(url_for('profile', username = username))


@app.route('/profile/<username>')
def profile(username): 
    ''' gets the uid of the profile, sees whether match is true so we know if the its the 
     session's own profile so the edit profile button can appear on their page '''
    conn = db.getConn(DB)
    uid = db.getUid(conn, username)
    #if not uid:
       # flash("User not found")
       # return render_template("home.html")
    uid=uid
    match = False
    
    if session['uid'] == uid: #if the session user is on their profile or someone elses
        match = True

    fullName = db.getFullName(conn, uid)
    bioText = db.getBioText(conn, uid)
    profPic = db.getPPic(conn, uid)
    posts = db.getPostsByUser(conn, uid)
    numPosts = db.numPostsUser(conn, uid)
    numFollowing = db.numFollowing(conn, uid)
    numFollowers = db.numFollowers(conn, uid)
   
    followingBoolean = db.following_trueFalse(conn, session['uid'], uid) #note that that a session username cannot follow itself, so jinja2 in profile.page will 
    #figure out whether the button should show up using match variable as well, it can carry over but it's used depending on the profile 

    if followingBoolean == True: #checks if there are already following that profile 
        buttonText = "Following"
    else:
        buttonText = "Follow"

    return render_template('profile.html', profName=username,
                                uid=uid, fname = fullName['fullname'], bio = bioText['biotxt'], 
                                ppic = profPic['profpicPath'], posts = posts, postNum = numPosts, 
                                match = match, numFing = numFollowing, numFers = numFollowers, tButton = buttonText)
                               

@app.route('/follow/<username>', methods= ["POST"])   
def aFollow(username):
    ''' ajax function adds a follower to the Follows table and updates the follower and following count and returns that as a jsonify '''
    try:
        conn = db.getConn(DB)
        profUID = db.getUid(conn, username)
        db.addfollower(conn, session['uid'], profUID)
        numFollowing = db.numFollowing(conn, profUID)
        numFollowers = db.numFollowers(conn, profUID)
        return jsonify(updateFollowers = numFollowers, updateFollowing= numFollowing)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )


@app.route('/unfollow/<username>', methods= ["POST"])   
def dFollow(username):
    ''' ajax function deletes a follower to the Follows table and updates the follower and following count and returns that as a jsonify '''
    try: 
        conn = db.getConn(DB)
        profUID = db.getUid(conn, username)
        db.deletefollower(conn, session['uid'], profUID)
        numFollowing = db.numFollowing(conn, profUID)
        numFollowers = db.numFollowers(conn, profUID)
        return jsonify(updateFollowers = numFollowers, updateFollowing = numFollowing)
    except Exception as err:
        print(err)
        return jsonify( {'error': True, 'err': str(err) } )

@app.route('/listofFollowers/<username>', methods = ["POST", "GET"])
def followersList(username):
    '''gets a list of users links that follow the current profile'''
    conn = db.getConn(DB)
    profUID = db.getUid(conn, username)
    users = db.followersUsers(conn, profUID)
    print(users)
    return render_template("listofFollowing.html", page_title="Followers of {}".format(username),users=users, options=False)

@app.route('/listofFollowing/<username>', methods = ["POST", "GET"])
def followingList(username):
    '''gets a list of users links that the current profile is following'''
    conn = db.getConn(DB)
    profUID = db.getUid(conn, username)
    users = db.followingUsers(conn, profUID)
    print(users)
    return render_template("listofFollowing.html", page_title="{} Following".format(username),users=users, options=False)

@app.route('/editprofile/', methods= ["POST", "GET"])
def editProf():
    '''gets info from the edit profile form and updates info accordingly '''
    uid = session['uid']
    username = request.form.get('pname')
    print("username " + username)
    fullName = request.form.get('displayName')
    biotext = request.form['bioText']

    conn = db.getConn(DB)

    #upload folder path, and allowed extension of file images
    UPLOAD_FOLDER = 'static/img/{}/'.format(uid)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

    #check allowed files 
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    #if 'file' not in request.files: 
            #flash('No file part')
            #return redirect('')

    file = request.files['profpic']
    filePath = None
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #get the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #save the file to the upload folder destination
            filePath = os.path.join('img/{}/'.format(uid), filename) #make a modified path so the profile.html can read it
            db.updateProfile(conn, uid, username, fullName, biotext, filePath) #update profile with new pic path
            return redirect(url_for('profile', username = username))
    else:
        #if not pic is uploaded, just upload the pre-filled data
        db.updateProfileNoPic(conn, uid, username, fullName, biotext)
        return redirect(url_for('profile', username = username))
   


# delete a post
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


# edit a post's name, resturant, location, rating, price, tags, review
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
    '''displays all posts under the given tag'''
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
                            options=False, tag=tag) 

# sort posts by rating no ajax, it's a serparate route for now
# this route is not being used in beta
@app.route('/sort_rating/', methods=["GET"])
def sort_rating():

    # better to send posts from ajax over and sort them using python sort
    # or get the posts again from the db sorted by rating?

    # posts = request.form.get("posts")

    query = request.values.get("query")
    
    if query[:-1] != "null":
        # get posts by query
        conn = db.getConn(DB)
        posts = db.getQueryPostsSortByRating(conn, query[:-1])
    else:
        # get all posts)
        conn = db.getConn(DB)
        posts = db.getAllPostsSortByRating(conn)
    
    return render_template("home.html", page_title="Results", posts=posts[::-1], options=True,
                                    query=query[:-1])


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