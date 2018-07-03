library(tseries)
library(ggplot2)
library(forecast)

finaluniverse <- c('ICICIBANK', 'BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'RECLTD','SRTRANSFIN','IDFC', 'DLF', 'CUMMINSIND', 'BRITANNIA', 'MARICO', 'NHPC', 'HINDPETRO', 'BAJAJHLDNG', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH', 'NBCC', 'JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN')

#ARMAtraining
for (i in 1:27)
{
  pdf1 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/training/",finaluniverse[i],".NS.csv", sep = ""))
  pdf2 <- read.csv(paste("/home/harsha/projects/R/Project_ideas/test/",finaluniverse[i],".NS.csv", sep = ""))
  print(finaluniverse[i])
  x <- pdf1$log_returns
  y <- pdf2$log_returns
  fit <- auto.arima(x)
  print(fit)
  fit_resid <- residuals(fit)
  #print()
  print(Box.test(fit_resid, lag = 10, type = 'Ljung-Box')) #lag 10 because it is non seasonal data
  predict <- forecast(fit, h = 246)
  #print(predict)
  pdf2[["ARIMA"]] <- predict[[4]]
  print(c(cor(pdf2$ARIMA, pdf2$log_returns, method="spearman"),'Correlation - Spearman'))
 # write.table(pdf2,paste("/home/harsha/projects/R/Project_ideas/armaforecast/",finaluniverse[i],".NS.csv", sep = ""), sep = ",", row.names = FALSE)
}

