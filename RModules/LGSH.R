require(reshape2)

SEED <- 1000
LGSH50 <- LDA(LGSH, k = 50, control = list(seed = SEED))
#LDA20 <- LDA(smalldtm, k = 20, control = list(seed = SEED))

# Welke termen zitten er in de topic?
trmLGSH50 <- terms(LGSH50, k = 20)
trmLGSH50

# Terms20 <- terms(LDA20, k = 50)
# Terms20

# Welke topics krijgen de documenten?
tpcLGSH50 <- topics(LGSH50, threshold = 0.2)
tpcLGSH50
# 
# Topics20 <- topics(LDA20, threshold = 0.05)
# Topics20


dfLGSH50 <- data.frame(word = do.call(c, tpcLGSH50),
                           group = rep(1:length(tpcLGSH50), 
                                       sapply(tpcLGSH50, length)))

melt(tpcLGSH50)
###############write.table(dfLGSH50, file = file.path(Rdir, "tpcLGSH50-v1.xls"), sep='\t',col.names = FALSE)
write.csv(trmLGSH50, file.path(Rdir, "LGSH50.csv"))
crps<- clean(fromJSON(file.path(PYdir, "LGSH.json")) %>% as.data.frame)
LGSHvis<-topicmodels_json_ldavis(LGSH50, crps, refine(crps))

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
