# database functions

import dbi

DSN = None

def getConn(DB):
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    conn = dbi.connect(DSN)
    conn.select_db(DB)
    return conn

def following_trueFalse(conn, sessionUid, profUid):
    '''Are you following this profile? Returns true or false'''
    curs = dbi.cursor(conn)
    curs.execute('''select * from Follows where follower_id=%s and followee_id=%s''', [sessionUid, profUid])
    return True if curs.fetchone() else False

def addfollower(conn, sessionUid, profUid):
    '''adds a follower to the Follows table to the current profile'''
    curs = dbi.dictCursor(conn)
    curs.execute('''INSERT INTO Follows(follower_id, followee_id)
                                VALUES(%s, %s)''', [sessionUid, profUid])

def deletefollower(conn, sessionUid, profUid):
    ''' deletes a follower from the Follows table of the current profile'''
    curs = dbi.dictCursor(conn)
    curs.execute('''DELETE from Follows where follower_id = %s and followee_id = %s''', [sessionUid, profUid])

def numPostsUser(conn, uid):
    '''computes the total posts for each user they have posted '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select count(*) from Posts where uid=%s''', [uid])
    result = curs.fetchone()
    return result['count(*)']

def numFollowing(conn, uid):
    ''' counts the number of users the current profile is following'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select count(*) from Follows where follower_id=%s''', [uid])
    result = curs.fetchone()
    return result['count(*)'] 

def followingUsers(conn, uid):
    '''lists the users who are the current profile is following'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select followee_id from Follows where follower_id=%s''', [uid])
    following = curs.fetchall()
    if len(following) == 0:
        return 0
    else:
        usersList = []
        for user in following:
            curs2 = dbi.dictCursor(conn)
            id = user['followee_id']
            curs2.execute('''select username from Users where uid=%s''', [id])
            usersList.append(curs2.fetchone())
       
        return usersList

 
def numFollowers(conn, uid):
    ''' counts the number of users following the current profile'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select count(*) from Follows where followee_id=%s''', [uid])
    result = curs.fetchone()
    return result['count(*)']

def followersUsers(conn, uid):
    '''lists the users that are following the current profile'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select follower_id from Follows where followee_id=%s''', [uid])
    followers = curs.fetchall()
    if len(followers) == 0:
        return 0
    else:
        usersList = []
        for user in followers:
            
            curs2 = dbi.dictCursor(conn)
            id = user['follower_id']
            
            curs2.execute('''select username from Users where uid=%s''', [id])
            usersList.append(curs2.fetchone())
        print("usersList " + str(usersList))
        return usersList


def like_trueFalse(conn, pid, uid):
    '''Are you following this profile? Returns true or false'''
    curs = dbi.cursor(conn)
    curs.execute('''select * from Likes where post_id=%s and profile_id=%s''', [pid, uid])
    return True if curs.fetchone() else False

def getUidfromPost(conn, pid):
    '''Given the post id (pid), get the uid of the post '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select uid from Posts where pid=%s''', [pid])
    result = curs.fetchone()
    return result['uid']

def countLikes(conn, pid):
    '''counts the number of likes a post has'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select count(*) from Likes where post_id=%s''', [pid])
    result = curs.fetchone()
    return result['count(*)']

def addLike(conn, pid, uid): 
    '''adds a like to the post into the Likes table'''
    curs = dbi.dictCursor(conn)
    curs.execute('''INSERT INTO Likes(post_id, profile_id)
                                VALUES(%s, %s)''', [pid, uid])
def removeLike(conn, pid, uid):
    '''removes a like to the post from the Likes table ''' 
    curs = dbi.dictCursor(conn)
    curs.execute('''DELETE from Likes where post_id=%s and profile_id=%s''', [pid, uid])

def likesList(conn, pid):
    '''lists the users that liked a particular post'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select profile_id from Likes where post_id=%s''', [pid])
    users = curs.fetchall()
    if len(users) == 0:
        return 0
    else:
        usersList = []
        for user in users:
            curs2 = dbi.dictCursor(conn)
            id = user['profile_id']
            curs2.execute('''select username from Users where uid=%s''', [id])
            usersList.append(curs2.fetchone())
        return usersList
''' COMMENTS mysql for comments, but not implemented...see app.py for more notes 
def getComments(conn, pid):
    gets the comment and who made the comment from the Comments table
    curs = dbi.dictCursor(conn)
    curs.execute(select comment, profile_id from Comments where post_id=%s, [pid])
    comments = curs.fetchall()
    if len(comments) == 0:
        return 0
    return comments

def addComment(conn, pid, uid, cText): 
    adds a comment to the Comments table
    curs = dbi.dictCursor(conn)
    curs.execute(INSERT INTO Comments(post_id, profile_id, comment)
                                VALUES(%s, %s,%s), [pid, uid, cText])


def deleteComment(conn, pid, uid, cText): 
    adds a comment to the Comments table
    curs = dbi.dictCursor(conn)
    curs.execute(DELETE from Comments where post_id=%s and profile_id=%s and comment=%s), [pid, uid, cText])
'''  

def getBioText(conn, uid):
    '''get the bio text from the database '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select biotxt from Users where uid=%s''', [uid])
    return curs.fetchone()

def getPPic(conn, uid):
    ''' get the pic path from the database '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select profpicPath from Users where uid=%s''', [uid])
    return curs.fetchone()

def getFullName(conn, uid):
    ''' get the full name from the database '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select fullname from Users where uid=%s''', [uid])
    return curs.fetchone()

def updateProfileNoPic(conn, uid, username, fname, text):
    '''update the profile of a given user '''
    curs = dbi.dictCursor(conn)
    curs.execute('''update Users set fullname=%s, biotxt=%s, username=%s where uid=%s''', [fname, text, username, uid])

def updateProfile(conn, uid, username, fname, text, path):
    '''update the profile of a given user '''
    curs = dbi.dictCursor(conn)
    curs.execute('''update Users set username=%s, fullname=%s, biotxt=%s, profpicPath=%s where uid=%s''', [username, fname, text, path, uid])

# get uid of a user by username
def getUid(conn, username):
    '''get uid given a username '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select uid from Users where username = %s''', [username])
    result = curs.fetchone()
    return result['uid']


# gets all posts for displaying posts in feed
def getAllPosts(conn):
    ''' get all the info for each post in the Posts table'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Posts''') # we don't need to get all change later
    return curs.fetchall() # change this later

# gets all posts in the db sorted by rating
def getAllPostsSortByRating(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Posts order by rating''') # we don't need to get all change later
    return curs.fetchall()

# get single post
def getSinglePost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select pname, rating, price, review, restaurant, location, imgPath, time, username
                     from Posts inner join Users on Users.uid=Posts.uid where Posts.pid = %s''', [pid])
    return curs.fetchone()

# gets posts that have tag 
def getPostsWithTid(conn, tid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select pname, Posts.pid, rating, price, review, restaurant, location, imgPath, time
                     from Posts inner join Tagpost on Posts.pid = Tagpost.pid where Tagpost.tid = %s ''',[tid])
    return curs.fetchall()

# get all tags of a post
def getTagsofPost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select ttype,Tags.tid from Tags inner join 
                            (select tid from Tagpost where
                            pid = %s) as t on t.tid = Tags.tid''',[pid])
    return curs.fetchall()
    
# returns posts where query matches post name, tag, restaurant, username, fullname
def getQueryPosts(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''(select * from Posts where pname like %s 
                            or restaurant like %s or location like %s)
                    union
                    (select Posts.* from Posts inner join 
                            (select pid from Tagpost inner join Tags 
                            on Tags.tid = Tagpost.tid where Tags.ttype = %s) as p 
                            on Posts.pid = p.pid)
                    union
                    (select Posts.* from Posts inner join (select uid from Users 
                            where username like %s or fullname like %s) as u
                            on Posts.uid = u.uid)''',
                ['%'+query+'%', '%'+query+'%', '%'+query+'%', query, 
                    '%'+query+'%', '%'+query+'%'])
    return curs.fetchall() # change to limit x offset y order by time

# returns posts where query matches post name, tag, restaurant, username, fullname
# sorted by rating
def getQueryPostsSortByRating(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''(select * from Posts where pname like %s 
                            or restaurant like %s or location like %s)
                    union
                    (select Posts.* from Posts inner join 
                            (select pid from Tagpost inner join Tags 
                            on Tags.tid = Tagpost.tid where Tags.ttype = %s) as p 
                            on Posts.pid = p.pid)
                    union
                    (select Posts.* from Posts inner join (select uid from Users 
                            where username like %s or fullname like %s) as u
                            on Posts.uid = u.uid) order by rating''',
                ['%'+query+'%', '%'+query+'%', '%'+query+'%', query, 
                    '%'+query+'%', '%'+query+'%'])
    return curs.fetchall()

# return users where query matches username, fullname
def getQueryUsers(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''select uid, fullname, email, username, biotxt, profpicPath
                        from Users where username like %s or fullname like %s''', 
                        ["%"+query+"%", "%"+query+"%"])
    return curs.fetchall()

# gets all posts by a user
def getPostsByUser(conn, uid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Posts where uid = %s''', [uid])
    return curs.fetchall()

# delete a post in the db 
def deletePost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''delete from Posts where pid = %s''', [pid])

# return all tag names in db
def getAllTags(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Tags''')
    return curs.fetchall()

# edit a post by its pid. can edit pname, restaurant, review
def editPost(conn, pid, pname, restaurant, location, rating, price, review):
    curs = dbi.dictCursor(conn)
    curs.execute('''update Posts set pname = %s, restaurant = %s, location=%s,
                        rating=%s, price=%s, review=%s where pid = %s''', 
                        [pname, restaurant, location, rating, price, review, pid])

#insert everything but filename and return the pid of the inserted image
def insertPost(conn, uid, name, rating, price, review, restaurant, location):
    #add to post table
    curs = dbi.dictCursor(conn)
    curs.execute(
        '''insert into Posts(uid,pname,rating,price,review,restaurant,location, time) 
        values (%s,%s,%s,%s,%s,%s,%s, now())''',
        [uid, name, rating, price, review, restaurant, location])
    curs.execute('''select last_insert_id() from Posts''')
    result = curs.fetchone()
    result = str(result['last_insert_id()'])
    return result
    
#inserts the image path named with the pid
def insertFilepath(conn, path, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''update Posts set imgPath = %s where pid = %s''',[path, pid])

# add a tag to a post by pid and tag id
def insertTagPost(conn, pid, tid):
    curs = dbi.dictCursor(conn)
    curs.execute('''insert into Tagpost(pid, tid) values(%s, %s)''', [pid, tid])

# delete a tag from a post if in db
def deleteTagPost(conn, pid, tag):
    curs = dbi.dictCursor(conn)

# get tag id of a tag by its tag type
def getTid(conn,ttype):
    curs = dbi.dictCursor(conn)
    curs.execute('''select tid from Tags where ttype=%s''',[ttype])
    return curs.fetchone()

# delete all tags of a post by pid
def deleteAllTagsofPost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''delete from Tagpost where pid=%s''', [pid])
