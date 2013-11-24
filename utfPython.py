import codecs
def file_contents(file_name):
    with codecs.open(file_name,encoding="utf-8") as f:
        try:
            return f.read()
        finally:
            f.close()

output=u'something more interesting here'
writer=open("my_out_file.txt",'w+') # w+ means overwrite - use with care
    writer.write(output.encode("UTF-8"))
writer.close()

exampleLookup <- function(path){
	text=system(paste0("python exampleLookup.py ",path),intern=T)
	return (text)
}
