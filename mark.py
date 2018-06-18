from set_mark.namu import namu

import re
import html
import sqlite3
from urllib import parse
import time
import threading

def load_conn2(data):
    global conn
    global curs

    conn = data
    curs = conn.cursor()

def send_parser(data):
    if not re.search('^<br>$', data):
        data = html.escape(data)
        
        javascript = re.compile('javascript:', re.I)
        
        data = javascript.sub('', data)
        data = re.sub('&lt;a href=&quot;(?:(?:(?!&quot;).)*)&quot;&gt;(?P<in>(?:(?!&lt;).)*)&lt;\/a&gt;', '<a href="' + parse.quote('\g<in>').replace('/','%2F') + '">\g<in></a>', data)
    
    return data
    
def plusing(name, link, backtype):
    curs.execute("select title from back where title = ? and link = ? and type = ?", [link, name, backtype])
    if not curs.fetchall():
        curs.execute("insert into back (title, link, type) values (?, ?, ?)", [link, name, backtype])

def namumark(title = '', data = '', num = 0):
    if not data == '':
        data = namu(conn, data, title, num)
        
        if num == 1:
            i = 0
            while 1:
                try:
                    _ = data[2][i][0]
                except:
                    break

                thread_start = threading.Thread(target = plusing, args = [data[2][i][0], data[2][i][1], data[2][i][2]])
                thread_start.start()
                thread_start.join()

                i += 1

            conn.commit()
            
        return data[0] + data[1]
    else:
        return '404 Not Found.'