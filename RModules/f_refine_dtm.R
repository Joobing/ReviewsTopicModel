refine<-function(corpusclean){
  
# Make the DTM for LDA:
dtm <-DocumentTermMatrix(corpusclean)

# Inspect the most frequent words (50 for normal here, 30 for LDA100)
highfreq <- findFreqTerms(dtm,40,Inf)
highfreq

# Kleinere DTM: woorden moeten meer dan 70 keer voorkomen óf in minstens 40 documents (30 and 20 resp. for LDA100)
smalldtm <- DocumentTermMatrix(corpusclean, control=list(dictionary = highfreq, bounds = list(global = c(10,Inf)))) # Terms that appear in <40 documents are discarded
rowTotals <- apply(smalldtm , 1, sum)
smalldtm   <- smalldtm[rowTotals> 0, ]
return(smalldtm)}