import sqlite3
import codecs
import os

#function to read files
def file_contents(file_name):
    with codecs.open(file_name,encoding="utf-8") as f:
        try:
            return f.read()
        finally:
            f.close()

#set up db - create new file if it doesn't exist yet
conn = sqlite3.connect('temp.db')                   #Initialize a connection
c = conn.cursor()                                   #create the cursor 'c'
try:
    c.execute("""                                   
                create table texts (
                id integer NOT NULL,
                file_name text NOT NULL,
                content text NOT NULL,
                PRIMARY KEY (id))
                """)
except:pass

folder="ovid"
fileList=os.listdir(folder)
counter=0                                                               #start a counter - this becomes document ID
for file_name in fileList:                                              #loop through file names
    counter+=1                                                          #Add 1 to the counter on each loop
    text = file_contents(folder+"\\"+file_name)                         #read in the files
    entry=((counter,file_name,text))                                    #make tuple called entry
    conn.execute("INSERT OR IGNORE INTO texts VALUES(?,?,?)",entry)     #SQL statement
    conn.commit()                                                       #Commit the statement


#the eagle eyed will have noted that this is a pretty inefficent method - we are entering texts into the database individually. We can use a list of entries instead; this gives a performance boost:
holder=[]                                                               #Holder is a list
for file_name in fileList:
    counter+=1
    text = file_contents(folder+"\\"+file_name)
    entry=((counter,file_name,text))
    holder.append(entry)                                                #Add each entry to the holder

conn.executemany("INSERT OR REPLACE INTO texts VALUES(?,?,?)",holder)   #Add all the entries in one go
conn.commit()                                                           #Don't forget to write the changes!

#Now, we may have many files to archive, so let's not assume they would all fit into memory; instead we will set the code to
#archive every 100 entries, and then reset the holder. To ensure that any residual texts are also entered, we keep the final executemany command:

holder=[]
for file_name in fileList:
    counter+=1
    text = file_contents(folder+"\\"+file_name)
    entry=((counter,file_name,text))
    holder.append(entry)
    if counter ==100:                                                               #When the counter reaches 100....
        conn.executemany("INSERT OR REPLACE INTO texts VALUES(?,?,?)",holder)       #we write the contents of the holder
        conn.commit()                                                               
        holder =[]                                                                  #Reset the holder
        counter=0                                                                   #Reset the counter
conn.executemany("INSERT OR REPLACE INTO texts VALUES(?,?,?)",holder)
conn.commit()

#get one entry:
ID,file_name,text=c.execute("SELECT id,file_name,content from texts").fetchone()

#get a specific entry
target="ovid_3.txt"
text=c.execute("SELECT content from texts WHERE file_name == '%s'" % target).fetchone()
#get all entries and do something with them

for ID,file_name,text in c.execute("SELECT id,file_name,content from texts").fetchall():
    print file_name
    #Do something more interesting here

#Now, what if the archive is really big? We can't fetch all texts. Instead, let's use a generator to yield a batch of files.
#This means we load  x (here:100) number of files, do something to these, load the next 100 files, etc. Consequently, we never have more than 100 files in memory at a given time

#This code is shamelessly stolen, I think from stackoverflow
def ResultIter(cursor, arraysize=100):
    'An iterator that uses fetchmany to keep memory usage down'
    counter=0
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            print "all data done"
            break
        for result in results:
            yield result

#The generator takes two inputs: the SQL statement, and the number of files to be retrieved in one go. Use it like this:
for ID,file_name,text in ResultIter(c.execute("SELECT id,file_name,content FROM texts")):
    print file_name
    #Do something more interesting here

#And that's that - now you have the necessary tools to archive a folder of files, and to retrieve them later.

            


#get x number of entries
