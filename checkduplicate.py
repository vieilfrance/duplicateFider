import hashlib
import os
from glob import glob
import sqlite3 as lite

checkpath='c:\Photos'
con = lite.connect('duplicates.db')

def hashfile(afile, hasher, fname, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    hashafile = hasher.hexdigest()
    addduplicate(fname,hashafile)

def initdatabase():
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS duplicates;")
        cur.execute("CREATE TABLE duplicates(id INTEGER PRIMARY KEY, path TEXT, hash TEXT);")
  
def addduplicate(path, hash):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO duplicates(path,hash) VALUES('"+path+"','"+hash+"');")

initdatabase()
fnamelst = [y for x in os.walk(checkpath) for y in glob(os.path.join(x[0], '*.jpg'))]
[(fname, hashfile(open(fname, 'rb'), hashlib.md5(),fname)) for fname in fnamelst]

