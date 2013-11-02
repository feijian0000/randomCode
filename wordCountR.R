fileList <- dir()

counter=NULL
for (i in fileList){
	text <- readLines(i,encoding="UTF-8")
	wordcount <- length(unlist(strsplit(text," ")))
	counter <- c(counter,wordcount)
}
