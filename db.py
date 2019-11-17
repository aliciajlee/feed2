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
