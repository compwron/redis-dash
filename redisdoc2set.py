#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

docpaths = ['redis.docset/Contents/Resources/Documents/commands', 'redis.docset/Contents/Resources/Documents/topics'] 
db = sqlite3.connect('redis.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

for docpath in docpaths:
    for fn in os.listdir(docpath):
        # Add page names 
        name = os.path.splitext(fn)[0]
        typ = os.path.split(docpath)[1] 
        
        if typ == 'commands': name = name.upper()  # Uppercase command names 
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'clm', '%s/%s' % (typ,fn)))
        print 'name: %s, path: %s/%s' % (name, typ, fn)
        
db.commit()
db.close()
