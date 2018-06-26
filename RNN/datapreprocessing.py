
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:19:03 2018

@author: tanishashrotriya
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


background = pd.read_csv("background.csv")
company_names=background.iloc[:,0].values
company_names


# In[ ]:



#declaring global dataframe
train_data=pd.DataFrame()


#removing nans for all symbols present
for sym in company_names :
    print(sym+".NS.csv")
    try:
        train = pd.read_csv(sym+".NS.csv")
        #getting the 8th column and all rows
        train_data=train.iloc[:,[8]].values
    
        print(np.any(np.isnan(train_data)))
        #setting all nas to zero
        np.nan_to_num(train_data,copy=False)
        print(np.any(np.isnan(train_data)))
        
        #saving the new text file or csv
        np.savetxt(sym+".NS.csv", train_data, delimiter=",")
        #not here it is going to overwrite 
    except :
        print("cool")
        
for sym in company_names :
    print(sym)
    try:
        print(np.any(np.isnan(train_data)))
    except :
        print("cool")
        


# In[8]:


#converting index to column and then to date time
#then resampling to new data set
universe = ['AARTIDRUGS', 'ABAN', 'ADVANIHOTR', 'ALBK', 'ALLCARGO', 'AMBIKCO', 'AMDIND', 'ASAHIINDIA', 'ASAL', 'ASHAPURMIN', 'ASIANHOTNR', 'ASTRAMICRO', 'BAJAJELEC', 'BAJAJHLDNG', 'BALAMINES', 'BALKRISIND', 'BBL', 'BBTC', 'BHARATRAS', 'BHARTIARTL', 'BHUSANSTL', 'BIL', 'BOMDYEING', 'BRITANNIA', 'BSELINFRA', 'CALSOFT', 'CANFINHOME', 'CELEBRITY', 'CESC', 'CHAMBLFERT', 'CIPLA', 'CLNINDIA', 'CONSOFINVT', 'COUNCODOS', 'CTE', 'CUMMINSIND', 'DCMSHRIRAM', 'DENORA', 'DHANBANK', 'DHFL', 'DICIND', 'DLF', 'DREDGECORP', 'EASUNREYRL', 'ECEIND', 'EIHOTEL', 'EIMCOELECO', 'ELECTHERM', 'ENIL', 'FDC', 'FEDERALBNK', 'FINCABLES', 'GAEL', 'GANDHITUBE', 'GARWALLROP', 'GATI', 'GEMINI', 'GESHIP', 'GKWLIMITED', 'GLOBALVECT', 'GLOBOFFS', 'GOLDIAM', 'GOLDINFRA', 'GREAVESCOT', 'GSS', 'GUFICBIO', 'HBLPOWER', 'HEIDELBERG', 'HEROMOTOCO', 'HIL', 'HINDOILEXP', 'HINDPETRO', 'HINDSYNTEX', 'HTMEDIA', 'ICICIBANK', 'IDFC', 'IFBAGRO', 'IIFL', 'INDIACEM', 'INDIANCARD', 'INDOTECH', 'INDSWFTLAB', 'INGERRAND', 'ITDCEM', 'IVRCLINFRA', 'JAINSTUDIO', 'JAYSREETEA', 'JINDALSTEL', 'JKCEMENT', 'JKTYRE', 'JYOTISTRUC', 'KAKATCEM', 'KANORICHEM', 'KEC', 'KERNEX', 'KNRCON', 'KOLTEPATIL', 'KPIT', 'LOKESHMACH', 'MADHUCON', 'MARALOVER', 'MARICO', 'MCDHOLDING', 'MEGASOFT', 'MMFL', 'MOTILALOFS', 'MRPL', 'MTNL', 'MUKANDENGG', 'NAHARPOLY', 'NAVINFLUOR', 'NDTV', 'NETWORK18', 'NIITLTD', 'NIPPOBATRY', 'NITINSPIN', 'NMDC', 'NUCLEUS', 'ORIENTLTD', 'PANACEABIO', 'PARACABLES', 'PATELENG', 'PBAINFRA', 'PDUMJEIND', 'PETRONENGG', 'PFC', 'PIONEEREMB', 'PITTILAM', 'PONNIERODE', 'PRAENG', 'PRAKASH', 'PUNJLLOYD', 'RANASUG', 'RECLTD', 'RELIGARE', 'RJL', 'RMCL', 'SAGCEM', 'SELAN', 'SHREYANIND', 'SHRIRAMEPC', 'SIYSIL', 'SKFINDIA', 'SOTL', 'SPARC', 'SRF', 'SRTRANSFIN', 'SSWL', 'STERTOOLS', 'SUNDARMFIN', 'SUNDRMFAST', 'SUNILHITEC', 'SUPREMEIND', 'SURANAT&P', 'SURYAROSNI', 'TANTIACONS', 'TATACOFFEE', 'TCI', 'TECHNO', 'TIL', 'TIMETECHNO', 'TIMKEN', 'TIRUMALCHM', 'TNPETRO', 'TNPL', 'TRENT', 'TRIVENI', 'TULSI', 'UNIONBANK', 'UNITY', 'VHL', 'VIJAYABANK', 'VIMTALABS', 'VSTIND', 'WELCORP', 'WENDT', 'WIPRO', 'WSTCSTPAPR', 'ZEEMEDIA', 'ZENITHEXPO', 'ZODJRDMKJ']

for sym in universe :
    try:
        print(sym)
        train= pd.read_csv(sym+".NS.csv")
        print(train.iloc[:10,[0,6]])
        train.set_index(train.iloc[:,0],inplace=True)
        train.index=pd.to_datetime(train.index)
        print(type(train.index))
        t=train.iloc[:,[6]]
        t=t.resample('W-MON').sum()
        t.iloc[:5,[0]]
        t.to_csv(sym+"pr.NS.csv")
        
    except:
        print("error")


# In[9]:


#create a file to note down the predictions 
pred=pd.read_csv("WIPROpr.NS.csv")
pred=pd.DataFrame(pred.iloc[len(pred)-90:,[0]].values,columns=["dates"])
print(pred)
pred.to_csv("pred.csv")


# In[10]:


for sym in universe :
    try:
        print(sym)
        train= pd.read_csv(sym+"pr.NS.csv")
        train=train.iloc[:,[1]]
        t=train.values
        #train.to_csv(sym+"pr.NS.csv")
        np.savetxt(sym+"pr.NS.csv", train, delimiter=",")
        
        
    except:
        print("error")


# In[12]:



train= pd.read_csv("SURANAT&P.NS.csv")
print(train.iloc[:10,[0,6]])
train.set_index(train.iloc[:,0],inplace=True)
train.index=pd.to_datetime(train.index)
#print(type(train.index))
t=train.iloc[:,[6]]
t=t.resample('W-MON').sum()
t.iloc[:5,[0]]
t.to_csv(sym+"pr.NS.csv")
t

