require(reshape2)

SEED <- 1000
PRSH50 <- LDA(PRSH, k = 50, control = list(seed = SEED))
#LDA20 <- LDA(smalldtm, k = 20, control = list(seed = SEED))

# Welke termen zitten er in de topic?
trmPRSH50 <- terms(PRSH50, k = 20)
trmPRSH50

# Terms20 <- terms(LDA20, k = 50)
# Terms20

# Welke topics krijgen de documenten?
tpcPRSH50 <- topics(PRSH50, threshold = 0.2)
tpcPRSH50
# 
# Topics20 <- topics(LDA20, threshold = 0.05)
# Topics20


dfPRSH50 <- data.frame(word = do.call(c, tpcPRSH50),
                           group = rep(1:length(tpcPRSH50), 
                                       sapply(tpcPRSH50, length)))

melt(tpcPRSH50)
###############write.table(dfPRSH50, file = file.path(Rdir, "tpcPRSH50-v1.xls"), sep='\t',col.names = FALSE)
write.csv(trmPRSH50, file.path(Rdir, "PRSH50.csv"))
PRSHvis<-topicmodels_json_ldavis(PRSH50, PRSH, clean(fromJSON(file.path(PYdir, "PRSH.json")) %>% as.data.frame))

# topicsframed <- data.frame(word = do.call(c, Topics20),
#                            group = rep(1:length(Topics20), 
#                                        sapply(Topics20, length)))


# melt(Topics20)
# write.table(topicsframed, file = "D:/#CULT/LDA20-v1.xls", sep='\t',col.names = FALSE)


#Miscellaneous from here:



##lets see if we can see the data
#corpusclean[[10]]
#dataframe<-data.frame(text=unlist(sapply(corpusclean, `[`, "content")), stringsAsFactors=F)
#write.table(dataframe, file = "C:/Users/S545493/Desktop/wordfreqHAGV.xls", sep='\t',row.names = FALSE)

#library(qdap)
#dataframecorpus<-as.data.frame(corpusclean)
#write.table(testDF, file = "C:/Users/S545493/Desktop/wordfreqHAGV.xls", sep='\t',col.names = FALSE)

#Stemming
#getStemLanguages()

#data <- data.frame(matrix(unlist(names), nrow=2035, byrow=T),stringsAsFactors=FALSE)
#data$topic90 <- I(Topicmult90)
#data$topic95 <- I(Topicmult95)
#data$topic100 <- I(Topicmult100)
#data$topic105 <- I(Topicmult105)
#data$topic110 <- I(Topicmult110)

#dfout <- data[1]
#dfout$topic <- data$topic95
#dfout$topic <- as.character(dfout$topic)
#dfout$topic <- gsub(":", "&", dfout$topic)

#topics <- terms(LDA95_2, 10)

#require(foreign)
#write.table(Topics50, file = "C:/Users/S545493/Desktop/LDA50.xls", sep='\t',row.names = FALSE)

#topicsdf <- data.frame(matrix(unlist(names), nrow=2035, byrow=T),stringsAsFactors=FALSE)

#write.table(topics, file = "C:/Users/u1232044/Desktop/topics105.xls", sep='\t',row.names = FALSE)

#gammaDF <- as.data.frame(LDA95_2@gamma) 
#names(gammaDF) <- c(1:2035)

# inspect...
#gammaDF$names <- LDA95_2@documents
#write.table(gammaDF, file = "C:/Users/RFJ/Desktop/posteriors.xls", sep='\t',row.names = FALSE)
