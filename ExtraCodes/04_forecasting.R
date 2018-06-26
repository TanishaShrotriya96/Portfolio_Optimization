## Let's study the time-series of Wipro daily returns
library(xts)
print(load("/home/tanishashrotriya/a/BLOCK1/demo_dailydata.rda"))

write.csv("/home/tanishashrotriya/a/BLOCK1/demo_dailydata.rda",file="myfile.csv")
r <- dailyreturns[,300]
head(dailyreturns[,300])
background

any(is.na(r))
plot(r); abline(h=0)
class(r)
#stripping from zoo to numeric -  casting
r <- as.numeric(r)
class(r)
length(r)

## ARMA models --
#auto correlation function
#null hypothesis at correlations nearing zero
acf(r)

#telling the ylimits, as we dont want the huge singular 1.0
plot(acf(r), ylim=c(-0.075,+0.075), lwd=5)
acf(r*r)
plot(acf(r*r), ylim=c(-0.2,+0.4), lwd=5)
pacf(r*r)
plot(acf(r*r), ylim=c(-0.2,+0.4), lwd=5)
pacf(r)
#blues are zone of rejection 
#when a big market is buying or selling then the prices will increase or go down
#patterns of correlation for high insti ownership vs lowinsti ownership

par(mfrow=c(2,2))
m <- ar(r)
#builds a test and train model
#output is a model object

## Realistically, how well are we forecasting?
m <- ar(r[1:2715])
predictions <- predict(m, n.ahead=16)$pred
#predict gives a dataframe
actuals <- r[2715:2730]
#this is the test data
together <- 100*cbind(predictions, actuals)
print(together, digits=2)
cor(predictions, actuals, method="spearman")

#decide what data is important

## Let's focus on the residual
#remove the ar data
e <- m$resid
head(e, 50)
e <- na.omit(e)
e
plot(e, type="h"); abline(h=0)
plot(density(e))

## There's quite some non-normality
#qqplot quintiles of normal distribution agaisnt quintiles of your data
qqnorm(e)
qqline(e)

?ar
k <- ar(r[1:2715],method=c("ols"),order.max=40,n.ahead=1,se.fit=TRUE)
predictions2 <- predict(k, n.ahead=1)$pred
actuals2 <-r[2715:2730]
together <- 100*cbind(predictions2, actuals2)
print(together, digits=2)
cor(predictions2, actuals2, method="spearman")
e <- k$resid
head(k, 50)
e <- na.omit(e)
e
plot(e, type="h"); abline(h=0)
plot(density(e))

## There's quite some non-normality
#qqplot quintiles of normal distribution agaisnt quintiles of your data
qqnorm(e)
qqline(e)
#financial markets are highly non-normal

??boxcox
library(MASS)
r
boxcox(k,plotit=TRUE)
## Runs test
#binary - up  and down 
#are the runs consistent with 50% probability for up and down

#install.packages("curls")
#install.packages("tseries")
library(tseries)
runs.test(factor(rnorm(3000) < 0))
# what are r factors
runs.test(factor(r < 0))
?runs.test
#install.packages("randtests")

library(randtests)
randtests::runs.test(r)

## My first machine learning
r <- dailyreturns[,300]
d <- r
for (i in 1:5) {
    d <- cbind(d, lag(r, -i))
}
head(d)
colnames(d) <- c("r",paste("r.l",1:5,sep=""))
head(d)
d <- na.omit(d)
head(d)
class(d)
d <- as.data.frame(d)

#install.packages("randomForest")
library(randomForest)
NROW(d)i
m <- randomForest(r ~ r.l1 + r.l2 + r.l3 + r.l4 + r.l5, data=d[1:2700,])
predictions <- predict(m, newdata=d[2701:2725,])
actuals <- as.numeric(d[2701:2725,1])
together <- 100*cbind(predictions, actuals)
print(together, digits=2)
cor(predictions, actuals, method="spearman")

#design clean ideas

## Numerous areas for further research.
## 1. Why only Wipro? Study all the firms.
##    We will be more confident in a set of AR coeffs if that
##    pattern shows up in many firms.

##    Does forecastability go up with less liquid firms?

## 2. When you do a 5% test for 100 firms, 5 will always reject.
##    Bring sophistication into how you think about the results.

## DONE I think?
## 3. Do thorough testbed: use data for 1..1000 to forecast 1001,
##    use 2..1001 to forecast 1002 and so on.
##    How to choose the estimation window?
##    E.g. Kalman-filter based thinking to look at changing AR coeffs.

## 4. Go intra-day!
##    Maybe there is more forecastability at lower frequency e.g. weekly?

## 5. Broaden the information set used in forecasting. E.g.
##    use the spot-futures basis.
