#================================================================

#how the size of the corporation impacts market cost

print(load("/home/tanishashrotriya/a/BLOCK1/demo_dailydata.rda"))

str(background)
## Stare at values for Wipro --
background[300,]
## The market cap is in million rupees at end-2015.
## The IC is for a micro-company, i.e. in this case Rs.1.37 million

summary(background)
background$meanIC <- .5*(background$buyIC - background$sellIC)
background$meanIC
## Stage 1: A simple graph
plot(background$nse_market_cap, background$meanIC)
#use log for clarity and removing the outliers or things which are unimportant
#box-cox transformation
plot(background$nse_market_cap, background$meanIC,
     log="xy")
background$lmeanIC <- log(background$meanIC)
background$lmktcap <- log(background$nse_market_cap)

#on average when company size goes up by 1% the IC goes down by 1/2

## Stage 2: OLS regression
summary(lm(lmeanIC ~ lmktcap, data=background))

## Stage 3: Loess (local regression) (builds a non linear function 1970s tech)
##(john tucky)
lomo <- loess(lmeanIC ~ lmktcap, data=background)
plot(lomo, xlab="log Mktcap", ylab="log IC")
#marketcap values
mvalues <- seq(4,14,.1)
mvalues
class(mvalues)
str(mvalues)
?seq
#predict is an R function which takes a model as input
predictions <- predict(lomo, data.frame(lmktcap=mvalues), se=TRUE)
#se stads for standard errors 
summary(predictions)
str(predictions)
head(predictions)
class(predictions)

lines(mvalues, predictions$fit, lwd=2, col="red")
lines(mvalues, predictions$fit - 2*predictions$se.fit, lwd=1, lty=2, col="red")
lines(mvalues, predictions$fit + 2*predictions$se.fit, lwd=1, lty=2, col="red")
#when you know less the uncertainty goes up, like on the edges

## Stage 4: Nonparametric regression
#install.packages("np")
library(np)
bw <- npregbw(formula = lmeanIC ~ lmktcap, data=background)
m <- npreg(bws = bw, gradients=TRUE)
plot(m, plot.errors.method="bootstrap", lwd=3)
points(background$lmktcap, background$lmeanIC, cex=.4, col="red")

## The zone of the strong decline is from lmktcap of 6 to 10
abline(v=c(6.3,9.5), col="blue", lty=2, lwd=2)
exp(6.3)
exp(9.5)


##+==============================================================================================

##checking for spreads at different times 

## Now let's turn to liquidity asymmetry
##is an R convention
background$is.buycheaper <- background$buyIC < -background$sellIC
summary(background$is.buycheaper)

## Let's look deeper into one security
library(zoo)
library(xts)
print(load("/home/tanishashrotriya/a/BLOCK2/demo_intradaydata.rda"))
source("/home/tanishashrotriya/a/BLOCK2/functions.R")
d <- data.stock.cash[[1]][[1]]
class(d)
str(d)
#tick data is dependent on the time when a new trade comes in and it is immediately updated
head(d)
## last traded price
# best buy price first
# best sell price 
# last traded qty

mean <- .5*(d[,"bbp1"] + d[,"bsp1"])
spreadpc <- 100*(d[,"bsp1"] - d[,"bbp1"])/mean
spreadpc <- zoo(spreadpc, order.by=index(d))
plot(spreadpc)
plot(head(spreadpc,2000))
plot(tail(spreadpc,2000))
