library(tseries)
library(ggplot2)
library(forecast)

finaluniverse <- c('ICICIBANK', 'BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'RECLTD','SRTRANSFIN','IDFC', 'DLF', 'CUMMINSIND', 'BRITANNIA', 'MARICO', 'NHPC', 'HINDPETRO', 'BAJAJHLDNG', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH', 'NBCC', 'JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN')

#ARMAtraining
for (i in 1:27)
{
  pdf1 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/armaforecast/",finaluniverse[i],".NS.csv", sep = ""))
  pdf2 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/test/",finaluniverse[i],".NS.csv", sep = ""))
  print(finaluniverse[i])
  x <- pdf1$ARIMA
  y <- pdf2$log_returns
  error = y-x
  print("RMSE")
  print(RMSE(error))
  rmsq <- c(RMSE(error),rmsq)
  print("MAE")
  print(mae(error))
  me <- c(mae(error),me)  
}

df1 <- data.frame(as.numeric(rmsq), as.numeric(me), index = finaluniverse)

write.csv(df1, "/home/harsha/projects/R/Project_ideas/armaforecast/rmsemae.csv", sep = ",", row.names = FALSE)


