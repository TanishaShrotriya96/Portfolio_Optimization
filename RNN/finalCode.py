
# coding: utf-8

# In[4]:


import pandas as pd
r=pd.read_csv("pred.csv")
r.to_csv("pred.csv")


# In[1]:


finalUniverse = [ 'NBCC','JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN','SUPREMEIND']
# add this'ICICIBANK','BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'OIL','RECLTD','SRTRANSFIN','IDFC' , 'DLF', 'CUMMINSIND','BRITANNIA', 'MARICO','NHPC', 'HINDPETRO', 
#errors not found 'BAJAJHLDNG', 'UNIONBANK', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH',


# In[2]:


count=0
ls=[]
for company in finalUniverse :
    try:
        import pandas as pd
        import numpy as np 
        import matplotlib.pyplot as plt

        testCount=246

        symbol=pd.read_csv(company+".NS.csv")
        print("Entire data count",len(symbol))
        train=symbol.iloc[:,len(symbol.columns)-2]
        print(train.head())
        print("last index", train.tail())
        print("Train data count",len(symbol))
        symbolTest=pd.read_csv(company+"test.csv")
        test=symbolTest.iloc[:,len(symbol.columns)-2]
        print(test.head())


        #get training data
        train1 = train
        train_data1=train1.iloc[:].values
        train_data1=train_data1.reshape(-1,1)
        #feature scaling - normalization  x-min(x)/max(x)-min(x)
        from sklearn.preprocessing import MinMaxScaler
        sc=MinMaxScaler(feature_range=(0,1))
        #fit means it will get the min and max stock price and then transform
        training_set_scaled1=sc.fit_transform(train_data1)

        #creating a recurrent neural network with 60 time steps before time t
        # and one output which is
        #stock price at time t

        #input ie 60 stock prices before financial day
        X_train1=[]
        #output ie stock price after financial day
        Y_train1=[]

        #note indices start at 0, so it will go from 0 to 59 and then we want i for Y_train
        for i in range(60,len(training_set_scaled1)) :
            X_train1.append(training_set_scaled1[i-60:i])
            Y_train1.append(training_set_scaled1[i])

        x_train1,y_train1=np.array(X_train1),np.array(Y_train1)

        #reshaping,  we are adding a dimension in a numpy array
        #we are only doing it on x_train
        #look at documentation of keras,recurrent layers and look up input shape
        x_train1=np.reshape(x_train1,(x_train1.shape[0],x_train1.shape[1],1))
        #number of rows,number of timesteps, number of indicators or parameters

        #building the RNN!! Stacked LSTM with layer
        #All models are wrong but some are useful!!

        from keras.models import Sequential
        from keras.layers import LSTM
        from keras.layers import Dense
        from keras.layers import Dropout

        #since we have continuous value so we are using regressor
        #initializing the RNN
        regressor1 = Sequential()

        #Let's add layers!

        #LAYER 1
        #dropout regularization to avoid overfitting
        regressor1.add(LSTM(units=50,return_sequences=True, input_shape=(x_train1.shape[1],1)))

        ##the first shape is considered automatically, and we only gice the remaining arguments
        ##we also enter the number of cells in the rnn to the network, 
        ##so it is the number of neurons per layer, so here it is 50
        ##return_sequence is true as there are also stacks to your lstm

        regressor1.add(Dropout(0.2))

        ##we drop out neurons to avoid overfitting, which is taken to be 20% of total neurons

        #LAYER 2

        ##remaining layer won't require an input layer
        ##since all neurons remain the same the shape of prev layer need not be specified
        regressor1.add(LSTM(units=50,return_sequences=True))
        regressor1.add(Dropout(0.2))
        #LAYER 3
        regressor1.add(LSTM(units=50,return_sequences=True))
        regressor1.add(Dropout(0.2))
        #LAYER 4
        regressor1.add(LSTM(units=50,return_sequences=False))
        regressor1.add(Dropout(0.2))
        ##false since it is the last layer before the output layer

        ##LAYER 5 ie output layer
        ##dense class is to make a full connection between ANN and CNN
        regressor1.add(Dense(units=1))

        ##compiling the RNN

        regressor1.compile(optimizer = "adam" ,loss = "mean_squared_error")

        ##fitting to training set
        ##epochs, how many tiimes you want to train
        ##batch size- weights are updated per batch and not per stock
        history=regressor1.fit(x_train1,y_train1,epochs =100,batch_size=32)

        regressor1
        ##########################################################################
        ##saving the fitted model 
        ##you will require sudo pip install h5py
        from keras.models import model_from_json

        model_json = regressor1.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        regressor1.save_weights("model.h5")
        
        print("Saved model to disk")

        #########################################################################

        # load json and create model
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model_json
        ########################################################################
        #importing stock price test data


        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")

        # evaluate loaded model on test data

        loaded_model.compile(optimizer = "adam" ,loss = "mean_squared_error")

        loaded_model
        model_from_json


        regressor1=loaded_model
        test1=test
        real_stock_price1=test1.iloc[:].values

        ##predicting 

        ##problem with concatenation of x_train
        ##- we require scaling, but then that will change the actual
        ##test values, since we have scaled the train with other train data
        ## so we will concatenate the original datasets
        ## and then we will scale, so then the actual values don't contain error

        dataset_total1=pd.concat((train1,test1), axis=0)

        #not the extra pair of brackets
        #axis is 0 as it is to be concatenated vertically, horizontally would be 1

        inputs1=dataset_total1[len(dataset_total1)-len(test1)-60:].values

        #we want Jan 3rd 2017, so we give calculated index
        #and we want numpy arrays so .values
        # we reshape to ensure we have the right numpy shape
        #always safe to do so

        inputs1=inputs1.reshape(-1,1)
        inputs1=sc.transform(inputs1)

        ##we don't fit again, as we want the same scaling as that of training method

        ##reshaping and creating the correct data structure
        X_test1=[]
        #note indices start at 0, so it will go from 0 to 59 
        ##20 financial days plus 60 previous values

        for i in range(60,testCount+60) :
            X_test1.append(inputs1[i-60:i,0])

        x_test1=np.array(X_test1)
        x_test1=np.reshape(x_test1,(x_test1.shape[0],x_test1.shape[1],1))

        ##prediction!!
        predicted_stock_price1=regressor1.predict(x_test1)
        #inverse the scaled predicted values so we can compare the actual with predicted
        predicted_stock_price1=sc.inverse_transform(predicted_stock_price1)

        predicted = pd.read_csv("pred.csv",index_col=0)
        df = pd.DataFrame(predicted_stock_price1,columns=[company])
        predicted=pd.concat([predicted, df[company]], axis=1)
        predicted.to_csv("pred.csv")  
        ###YAY! let's plott!!

        plt.plot(real_stock_price1,color="red",label="20 days Real Google Stock Price")
        plt.plot(predicted_stock_price1,color="blue",label="20 days Predicted Google Stock Price")
        plt.title("Comparison of Google Stock Price Prediction")
        plt.xlabel("Time")
        plt.ylabel("Google Stock Price")
        plt.legend()
        plt.show()

        # use the default conversion rules to which the pandas conversion
        # is added

        from sklearn.metrics import mean_squared_error 
        from math import sqrt
        
        ls.append(sqrt(mean_squared_error(real_stock_price1,predicted_stock_price1)))  
      
    except:
        count=count+1
        print("ERROR")


# In[3]:


ls


# In[ ]:


import pandas as pd

r=pd.read_csv("real.csv")
p=pd.read_csv("pred.csv")


