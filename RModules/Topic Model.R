PYdir<-Rdir<-"M:/#CULT"
#!cmd: C:\Program Files\R\R-4.0.2\bin>start rstudio.exe --max-mem-size=10GB

# source(file.path("M:", "f_file_replace.r") , echo = TRUE)
#for (id in list("TMLN", "PRSH", "PRLN", "LGSH", "LGLN"))#source_path, target_path, pattern, replacement
#{ replace<-list("TMSH" = id); file_find_replace(file.path(Rdir, "TMSH.R"), file.path(Rdir, paste(id, ".R", sep="")), replace);}



#Preparing for the topic model
#In WindowsPowercell use the command Get-ChildItem | Ren -NewName {"WATERSCHAPSNAAM" + $_.Name + $_.extension}
#Then use the command gci *.txt | rename-item -newname { [string]($_.name).substring(NUMBER OF LETTERS THE WATERSCHAPSNAAM IS) }

#require(devtools)
#library(devtools)
#install_github("bstewart/stm",dependencies=TRUE)
#require(Rstem)
require(tm) 
require(NLP)
require(SnowballC)
require(XML)
require(stringi)
require(RTextTools)
require(topicmodels)
require(stringr)
require(plyr)
require(foreign)
require(ldatuning)
require(jsonlite)

gc()
memory.limit()
memory.size()

#memory.limit(size = 250000)
memory.size(max = TRUE)
source(file.path(PYdir, "f_clean.R"))
source(file.path(PYdir, "f_refine_dtm.R"))

# source(file.path(PYdir, "TMLN.r") , echo = TRUE)
# source(file.path(PYdir, "TMSH.r") , echo = TRUE)
# source(file.path(PYdir, "LGLN.r") , echo = TRUE)
# source(file.path(PYdir, "LGSH.r") , echo = TRUE)
# source(file.path(PYdir, "PRLN.r") , echo = TRUE)
# source(file.path(PYdir, "PRSH.r") , echo = TRUE)


TMSH<-fromJSON(file.path(PYdir, "TMSH.json")) %>% as.data.frame
PRSH<-fromJSON(file.path(PYdir, "PRSH.json")) %>% as.data.frame
LGSH<-fromJSON(file.path(PYdir, "LGSH.json")) %>% as.data.frame
TMLN<-fromJSON(file.path(PYdir, "TMLN.json")) %>% as.data.frame
PRLN<-fromJSON(file.path(PYdir, "PRLN.json")) %>% as.data.frame
LGLN<-fromJSON(file.path(PYdir, "LGLN.json")) %>% as.data.frame




TMSH<- refine(clean(TMSH))
PRSH<- refine(clean(PRSH))
LGSH<- refine(clean(LGSH))
TMLN<- refine(clean(TMLN))
PRLN<- refine(clean(PRLN))
LGLN<- refine(clean(LGLN))

# 
for(smalldtm in list(TMSH, TMLN, PRSH, PRLN, LGSH, LGLN)){
#finding the appropriate number of topics:
result <- FindTopicsNumber(
  smalldtm,
  topics = seq(from = 25, to = 100, by = 25),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed = 77),
  mc.cores = 1L,
  verbose = TRUE
)
FindTopicsNumber_plot(result)}

# for (id in list("TMSH.r", "PRSH.r")){source(file.path(Rdir, id) , echo = TRUE)}
for (id in list("TMLN.r", "PRLN.r", "LGLN.r")){source(file.path(Rdir, id) , echo = TRUE)}

write.csv(trmPRLN50, file.path(Rdir, "PRLN50.csv"))
write.csv(trmTMLN50, file.path(Rdir, "TMLN50.csv"))
write.csv(trmLGLN50, file.path(Rdir, "LGLN50.csv"))

#How to get an overview of words:
#tdmalltxt <- TermDocumentMatrix(corpusclean,control=list(bounds = list(global = c(1,Inf))))
#
#wordfreq <- rowSums(as.matrix(tdmalltxt))
#testDF <- data.frame(as.list(wordfreq))
#testDF <- t(testDF)
#write.table(testDF, file = "C:/Users/S545493/Desktop/wordfreqWS.xls", sep='\t',col.names = FALSE)


# convert pdf to txt
#folder <- "F:\\Uvt - Seagate\\Research\\Dissertation\\Project 2_Collaboration and implementation of BMC\\Data\\Name of Waterschap"
#length <- length(dir(folder))
#dirpdf <- (dir(folder))
#pdftotxt <- "D:\\PDF to TXT\\xpdfbin-win-3.04\\bin32\\pdftotext.exe"
#for(i in 1:length(dir(folder)))
#{
#  pdf<-file.path("F:\\Uvt - Seagate\\Research\\Dissertation\\Project 2_Collaboration and implementation of BMC\\Data\\Name of Waterschap", dirpdf[i])
#  system(paste("\"", pdftotxt, "\" \"", pdf, "\"", sep = ""), wait = F)
#}


#myfiles <- list.files(path=dest, recursive = TRUE, pattern = NULL,full.names=TRUE)
# lapply(myfiles,function(i) system(paste('"D:\\PDF to TXT\\pdf-to-text.exe"'
# txt <- system.file("texts", "F:\\Uvt - Seagate\\Research\\Dissertation\\Project 2_Collaboration and implementation of BMC\\Data\\", package = "tm")
