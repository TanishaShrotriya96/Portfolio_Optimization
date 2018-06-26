#Compare the classification performance of linear regression and k–
#nearest neighbor classification on the zipcode data. In particular, consider
#only the 2 ’s and 3 ’s, and k = 1, 3, 5, 7 and 15. Show both the training and
#test error for each choice. The zipcode data are available from the book
#website www-stat.stanford.edu/ElemStatLearn .

#load data from training to data frame
?read.table
train<-as.data.frame(read.table("/home/tanishashrotriya/Downloads/zip_train"))
dim(train)
summary(train)

#removing values for second and third
second<-subset(train, train$V1==2)
third<-subset(train, train$V1==3)
toTrain<-rbind(second,third)

#load data from test set
test<-as.data.frame(read.table("/home/tanishashrotriya/Downloads/zip_test"))

#separating second and third here too
secondT<-subset(test, test$V1==2)
thirdT<-subset(test, test$V1==3)
n<-rbind(secondT,thirdT)
dim(n)

#==================================================================================
#Linear Regression Model

#calculating beta values for ols
beta<-lm(V1~., data= toTrain)
class(beta)
str(beta)

#make a prediction

#checking the actual value at column 2003
n["2003",1]
predict(beta,n,se.fit=TRUE)
# we see that an error factor exists

#==================================================================================
#K-Nearest Neighbours Model

install.packages("class")
library(class)
prediction1<-knn(train=train[,-1],test=test[,-1],cl=train[,1],k=1)
prediction3<-knn(train=train[,-1],test=test[,-1],cl=train[,1],k=3)
prediction5<-knn(train=train[,-1],test=test[,-1],cl=train[,1],k=5)
prediction7<-knn(train=train[,-1],test=test[,-1],cl=train[,1],k=7)
prediction15<-knn(train=train[,-1],test=test[,-1],cl=train[,1],k=15)

install.packages("gmodels")
library(gmodels)
CrossTable(x=test[,1],y=prediction1,prop.chisq = FALSE)
CrossTable(x=test[,1],y=prediction3,prop.chisq = FALSE)
CrossTable(x=test[,1],y=prediction5,prop.chisq = FALSE)
CrossTable(x=test[,1],y=prediction7,prop.chisq = FALSE)
CrossTable(x=test[,1],y=prediction15,prop.chisq = FALSE)

#TUTORIAL FOLLOWED
#https://www.analyticsvidhya.com/blog/2015/08/learning-concept-knn-algorithms-programming/