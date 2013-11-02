import codecs
import time
def file_contents(file_name):
    with codecs.open(file_name,encoding="utf-8") as f:
        try:
            return f.read()
        finally:
            f.close()

file_name= "your_file_here"
time1=time.time()
for i in range(1):
    d = file_contents(file_name)
    wc=len(d.split())
time2=time.time()
print str(time2-time1)
