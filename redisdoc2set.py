#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('redis.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpaths = ['redis.docset/Contents/Resources/Documents/commands', 'redis.docset/Contents/Resources/Documents/topics'] 

for docpath in docpaths:
    for fn in os.listdir(docpath):
        
        fn = fn.strip()
        name = os.path.splitext(fn)[0].strip()
        typ = os.path.split(docpath)[1].strip() 
        if typ == 'commands': name = name.upper()  # Uppercase command names as in the Redis docs 
        
        # Add title tags to pages
        html = open('%s/%s' % (docpath, fn),'r').read()
        html = '<TITLE>Redis: %s</TITLE>\n%s' % (name, html)
        open('%s/%s' % (docpath, fn),'w').write(html)

        if len(name) > 0 and name not in ('sponsors', 'whos-using-redis'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'clm', '%s/%s' % (typ,fn)))
            print 'name: %s, path: %s/%s' % (name, typ, fn)
        
db.commit()
db.close()
