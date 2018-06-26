## An imaginary returns time-series
r <- rnorm(10, sd=3, mean=.1)
r
plot(r, type="h", lwd=5, xlab="Days", ylab="Returns (Per cent)")
abline(h=0)
plot(r, type="h", lwd=5, xlab="Seconds", ylab="Returns (Per cent)")
abline(h=0)

## From returns to prices
r <- 1+(r/100)
r
c(100,r)
p <- cumprod(c(100,r))
p
plot(p, xlab="Seconds", type="l", lwd=2, ylab="Rupees")

## From prices back to returns
100*diff(log(p))
cbind(100*(r-1), 100*diff(log(p)))

##Basically you have just plotted the rate of the nifty index vs the year
## Let's go into some real data
library(xts)
print(load("/home/tanishashrotriya/a/BLOCK1/demo_dailydata.rda"))
str(background)
NROW(background)
head(background)
ncol(background)

str(dailyreturns)
NROW(dailyreturns)
ncol(dailyreturns)
head(dailyreturns)
nrow(background$symbol)

#install.packages("stringi")
#library(stringi)
#str_extract(background$symbol,"GOLDMAN")
## Let's find Wipro

str(dailyreturns)
subset(background, background$symbol=="WIPRO")
colnames(dailyreturns)[300]
r <- dailyreturns[,300]
r
## or
r <- dailyreturns[,"WIPRO"]
r
any(is.na(r))
plot(r); abline(h=0)
head(r)
head(1+r)
c(100, head(1+r))
cumu<-cumprod(c(100, head(1+r)))
cumu
plot(cumprod(c(100, head(1+r))), type="l", xlab="days", ylab="Price index")
plot(cumprod(c(100, 1+r)), type="l", xlab="days", ylab="Price index")
plot(cumprod(c(100, 1+r))[-1], type="l", xlab="days", ylab="Price index")

## let's get the dates back in
tmp <- cumprod(c(100, 1+r))
#removes the first index value
tmp <- tmp[-1]
head(tmp)
tmp <- zoo(tmp, order.by=index(r))
head(tmp)
#zoo automatically uses internal functions to get a good x-axis
plot(tmp, xlab="", ylab="Price index")


## Now let's turn to BLOCK2
print(load("/home/tanishashrotriya/Downloads/summer2018/a/BLOCK2/demo_intradaydata.rda"))
## So we have to decipher
##    background
##    data.nifty
##    data.stock.cash
##    data.stock.futures

class(background)
str(background)
background

str(data)
class(data)
data
class(data.nifty)
str(data.nifty)                # 4 lists each containing stock prices of nifty 
                               #and nifty junior of 4 days
head(data.nifty[[2]])
data.nifty[[2]]
class(data.stock.cash)                  # There are 15 companies
str(data.stock.cash)
str(data.stock.cash[[2]])
str(data.stock.cash[[1]])               # This is TCS, there are 4 days
tcs <- data.stock.cash[[1]]             # This is the 1st day of TCS
tcs[[1]]
head(tcs[[1]])
data.nifty[[1]]
plot(tcs[[1]][,"ltp"])
tcs[[1]][1:2,"ltp"]
class(data.stock.futures)
str(data.stock.futures)
summary(data.stock.futures)
tcs.f <- data.stock.futures[[1]]
str(tcs.f)
tcs.f.day1 <- tcs.f[[1]]
str(tcs.f.day1)
summary(tcs.f.day1)
head(tcs.f.day1[,1])
tcs.f.day1
plot(tcs.f.day1[,"ltp"])
class(data.nifty)

## Now let's do some examples of using this data
source("/home/tanishashrotriya/Downloads/summer2018/a/BLOCK2/functions.R")

## Plot of Nifty level at tick frequency, for one day
## note that the index itself is the timestamp so you just need to give one of the two rows
data.nifty[[1]]$nifty
par(mfrow=c(1,2))
plot (data.nifty[[1]]$nifty/100,
      type = "l",
      main = "Nifty index",
      ylab = "Nifty index")

## Plot of Nifty at a 5min resolution
##Nifty index differenced by five minutes
nifty.values <- intervalData(name = "nifty",
                             instrument = NULL, interval = "300")
plot (nifty.values[[1]]$nifty/100,
      type = "l",
      main = "Nifty index",
      ylab = "Nifty index")

## Superpose TCS spot and futures for one day
spot <- tcs[[1]][,"ltp"]
futures <- tcs.f.day1[,"ltp"]
both <- cbind(spot,futures)
both
plot(as.zoo(both), plot.type="single", col=c("black","red"))


