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


def getAllPosts(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from Posts''')
    return curs.fetchall() # change this later

# returns posts where query matches post name, tag, restaurant,
def getQueryAll(conn, query):
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
