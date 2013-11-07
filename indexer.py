import os
import sqlite3
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in
from whoosh.query import Term
from whoosh.qparser import QueryParser
from whoosh import highlight

from pymongo import Connection
from bson.objectid import ObjectId

def ResultIter(cursor, arraysize=10):
    'An iterator that uses fetchmany to keep memory usage down'
    counter=0
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            print "all data done"
            break
        for result in results:
            yield result

 
# Set index, we index title and content as texts and tags as keywords.
# We store inside index only titles and ids.
schema = Schema(content=TEXT,
                nid=ID(stored=True), fileName=KEYWORD(stored=True))
 
# Create index dir if it does not exists.
if not os.path.exists("index"):
    os.mkdir("index")
 
# Initialize index
index = create_in("index", schema)
 
# Initiate db connection
conn = sqlite3.connect('temp.db')
c = conn.cursor()

# Fill index with posts from DB
writer = index.writer()
for entry in ResultIter(c.execute("SELECT id,file_name,content FROM texts")):
    ID,file_name,text =entry
    writer.add_document(content=unicode(text),
                           nid=unicode(ID),
                           fileName=file_name)
writer.commit()

# Search inside index for post containing "test", then it displays
# results.
qp = QueryParser("content", schema=index.schema)

def printResults(result):
    for i in result:
        print i["nid"]

def printHighlights(result,surround):
    result.fragmenter.surround = surround
    result.formatter=highlight.UppercaseFormatter()
    for i in result:
        target=i["nid"]
        print "hits from "+str(i["fileName"])+":"
        t=c.execute("SELECT content from texts WHERE id == '%s'" % target).fetchone()
        print i.highlights("content",text=unicode(t))
            
#for single term
with index.searcher() as searcher:
    result = searcher.search(Term("content", u"nec"))
    #printResults(result)
    #printHighlights(result,50)

print "ok"
#for phrase and a limited number of hits
with index.searcher() as searcher:
    result= searcher.search(qp.parse(u"nec tibi vitetur"),limit=20) 
    printResults(result)

#And using wildcards phrase and a limited number of hits
with index.searcher() as searcher:
    result= searcher.search(qp.parse(u"nec tibi vitetur"),limit=20) 
    printResults(result)




def getResults(searchPhrase,nHits,surround):
    with index.searcher() as searcher:
        if len(searchPhrase.split())==1:
            result = searcher.search(Term("content", unicode(searchPhrase)))
        else: 
            result= searcher.search(qp.parse(unicode(searchPhrase),limit=20))
        printResults(result)
        printHighlights(result,surround)
        #1print result["nid"]
