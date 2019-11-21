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
    curs.execute('''select count(*) from Posts''')
    result = curs.fetchone()
    return result['count(*)']
    
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

# for displaying posts in feed
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

# returns posts where query matches post name, tag, restaurant,
def getQueryPosts(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''(select * from Posts where pname like %s 
                                            or restaurant like %s
                                            or location like %s)
                    union
                    (select Posts.pid, uid, pname, rating, price, review, restaurant, location, imgPath, time 
                                            from Posts inner join 
                                            (select pid from Tagpost inner join Tags 
                                            on Tags.tid = Tagpost.tid 
                                            where Tags.ttype like %s) as p 
                                            on Posts.pid = p.pid)''', ['%'+query+'%', '%'+query+'%', '%'+query+'%', query])
    return curs.fetchall() # change to limit x offset y order by time

# return users where query matches username
def getQueryUsers(conn, query):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Users where username like %s''', ["%"+query+"%"])
    return curs.fetchall()
