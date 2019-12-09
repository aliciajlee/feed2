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

def getNumPosts(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select max(pid) from Posts''')
    result = curs.fetchone()
    return result['max(pid)']
    
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

def updateProfile(conn, uid, fname, text, path):
    '''update the profile of a given user '''
    curs = dbi.dictCursor(conn)
    curs.execute('''update Users set fullname=%s, biotxt=%s, profpicPath=%s where uid=%s''', [fname, text, path, uid])

# get uid of a user by username
def getUid(conn, username):
    curs = dbi.dictCursor(conn)
    print(username)
    curs.execute('''select uid from Users where username = %s''', [username])
    return curs.fetchone()

# gets all posts for displaying posts in feed
def getAllPosts(conn):
    '''select all the posts '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Posts''') # we don't need to get all change later
    return curs.fetchall() # change this later

# get single post
def getSinglePost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select pname, rating, price, review, restaurant, location, imgPath, time, username
                     from Posts inner join Users on Users.uid=Posts.uid where Posts.pid = %s''', [pid])
    return curs.fetchone()

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

# return users where query matches username, fullname
def getQueryUsers(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Users where username like %s or fullname like %s''', 
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
    curs.execute('''select tid from Tagpost where ttype=%s''',[ttype])
    return curs.fetchone()

# delete all tags of a post by pid
def deleteAllTagsofPost(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''delete from Tagpost where pid=%s''', [pid])
