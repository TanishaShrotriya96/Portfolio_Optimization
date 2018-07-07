library(tseries)
library(ggplot2)
library(forecast)

finaluniverse <- c('ICICIBANK', 'BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'RECLTD','SRTRANSFIN','IDFC', 'DLF', 'CUMMINSIND', 'BRITANNIA', 'MARICO', 'NHPC', 'HINDPETRO', 'BAJAJHLDNG', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH', 'NBCC', 'JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN')
armacorrelation <- list()
rnncorrelation <- list()
rnnall <- read.csv(paste("/home/harsha/projects/R/Project_ideas/rnnforecast/rnnlogreturns.csv", sep = ""))
#ARMAcorrelation
for (i in 1:27)
{
  pdf1 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/armaforecast/",finaluniverse[i],".NS.csv", sep = ""))
  pdf2 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/test/",finaluniverse[i],".NS.csv", sep = ""))
  print(finaluniverse[i])
  x <- pdf1$ARIMA
  y <- pdf2$log_returns
  armacorrelation <- c((cor(x, y, method="spearman")),armacorrelation)
  
}
#RNNcorrelation
for (i in 1:27)
{
  pdf1 <- rnnall[[i]]
  pdf2 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/test/",finaluniverse[i],".NS.csv", sep = ""))
  print(finaluniverse[i])
  x <- pdf1
  y <- pdf2$log_returns[-1]
  rnncorrelation <- c((cor(as.numeric(x), as.numeric(y), method="spearman")),rnncorrelation)
  
}

df1 <- data.frame(as.numeric(rnncorrelation), as.numeric(armacorrelation), index = finaluniverse)

write.csv(df1, "/home/harsha/projects/R/Project_ideas/rnnforecast/CORRELATION.csv", sep = ",", row.names = FALSE)
