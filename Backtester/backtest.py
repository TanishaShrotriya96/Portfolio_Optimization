import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA
from arch import arch_model
from scipy.stats import spearmanr
from scipy.stats import pearsonr

#resample = 1
#lookback = 4
#lookback2 = 2

init_value = 100000

start_date = '2013-04-01'   #FLAG
end_date = '2017-03-31'	  #FLAG
start_date2 = '2017-04-01'
end_date2 = '2018-03-31'
daterange2 = pd.date_range(start_date2,end_date2)

df = pd.DataFrame(index = daterange2)



#Universe = symbols of all the stocks considered for the study.
universe = ['ICICIBANK', 'BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'RECLTD','SRTRANSFIN','IDFC', 'DLF', 'CUMMINSIND', 'BRITANNIA', 'MARICO', 'NHPC', 'HINDPETRO', 'BAJAJHLDNG', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH', 'NBCC', 'JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN']






def load_forecast_data(stock_list,daterange):
	ln_rt = pd.DataFrame(index = daterange) 
	for symbol in stock_list:
		pdf = pd.read_csv("~/projects/R/Project_ideas/armaforecast/{}.NS.csv".format(symbol), index_col = "Date", parse_dates = True, usecols = ['Date','ARIMA'], na_values = 'NA') 
		pdf.columns = [symbol]
		ln_rt = ln_rt.join(pdf)
		
	return ln_rt.dropna()
	
#volume	
def load_real_data(stock_list,daterange):
	ln_rt = pd.DataFrame(index = daterange) 
	for symbol in stock_list:
		pdf = pd.read_csv("~/projects/R/Project_ideas/test/{}.NS.csv".format(symbol), index_col = "Date", parse_dates = True, usecols = ['Date','log_returns'], na_values = 'NA')
		pdf.columns = [symbol]
		ln_rt = ln_rt.join(pdf)
		
	return ln_rt.dropna()


def resamplesum(array,resample): #resample the data every 'resample' number of days
	ln_rt = array.resample('{}D'.format(resample), how='sum')
	return ln_rt



def weight(forecast,x):
	ln_rt_np = forecast.values
	weightdf = pd.DataFrame((ln_rt_np), index = forecast.index, columns = universe)	
	return weightdf
	
def weightsharpe(forecast,x,universe,rfr,ln_rt):
	weight = np.zeros((246,27))
	forecastnp = np.array(forecast.values)
	lnrtnp = ln_rt.values
	print forecastnp.shape
	for i in range(0,27):
		for j in range(0,246):	
			if (forecastnp[j,i]!=0):
				weight[j,i] = (np.sum(forecastnp[0:,i], axis = 0)-rfr/100)/np.std(lnrtnp[0:,i])/pow(246,0.5)
			else:
				weight[j,i] = 0
	#print weight
	return weight
	

def portfolioarma(init_value,final_weight,ln_rt,universe, daterange):
	final_weight_long = final_weight.values
	final_weight_long = final_weight_long.clip(0)
	returns_long_net = ln_rt.values*final_weight_long
	daily_ret_long = np.sum(returns_long_net,axis=1)
	daily_ret_long = pd.DataFrame(daily_ret_long,index = daterange )
	cumulative_ret_long = daily_ret_long.cumsum()
	cumulative_PNL_long = (np.exp(np.array((cumulative_ret_long.values)))-1)*init_value
	pnldf = pd.DataFrame(cumulative_PNL_long, index = daterange, columns = ["PNL"])
	pnldf.plot()
	plt.title("PNL - ARIMA")
	plt.xlabel('Date')
	plt.ylabel('PNL in Rs')
	plt.legend(("PNL",))
	plt.savefig("/home/harsha/projects/R/plots/arima2.png")
	plt.show()
	
	print "\n\nARIMA forecast performance:"	
	print "Initial investment: Rs {}".format(init_value)
	print "Net PNL: Rs ", pnldf.values[-1]
	print "CAGR = {} %".format((pnldf.values[-1]/init_value)*100)
	print "Sharpe ratio of portfolio(annualized) : {}".format(np.std(np.array(daily_ret_long.values))*pow(246,0.5))
	print "\n\n"	
	
def portfoliornn(init_value,final_weight,ln_rt,universe, daterange):
	final_weight_long = final_weight.values
	final_weight_long = final_weight_long.clip(0)
	returns_long_net = ln_rt.values[1:,]*final_weight_long
	daily_ret_long = np.sum(returns_long_net,axis=1)
	daily_ret_long = pd.DataFrame(daily_ret_long,index = daterange )
	cumulative_ret_long = daily_ret_long.cumsum()
	cumulative_PNL_long = (np.exp(np.array((cumulative_ret_long.values)))-1)*init_value
	pnldf = pd.DataFrame(cumulative_PNL_long, index = daterange, columns = ["PNL"])
	pnldf.plot()
	plt.title("PNL - RNN")
	plt.xlabel('Date')
	plt.ylabel('PNL in Rs')
	plt.legend(("PNL",))
	plt.savefig("/home/harsha/projects/R/plots/rnn2.png")
	plt.show()
	
	print "\n\nRNN forecast performance:"	
	print "Initial investment: Rs {}".format(init_value)
	print "Net PNL: Rs ", pnldf.values[-1]
	print "CAGR = {} %".format((pnldf.values[-1]/init_value)*100)
	print "Sharpe ratio of portfolio(annualized) : {}".format(np.std(np.array(daily_ret_long.values))*pow(246,0.5))
	print "\n\n"



#neutralization type: 0 - none, 1 - index
def neutralize(weight,n_type,stock_list,tempdate):
	mean = pd.DataFrame(index = tempdate)
	mean = weight.mean(axis = 0)
	#print mean
	total_array = pd.DataFrame(index = tempdate)
	scale_array = pd.DataFrame(index = tempdate)
	scale_array = abs(weight).max(axis = 1)
	
	#print total_array
		
	total_array = abs(weight).sum(axis = 1)
	if (n_type == 0):
		for column in weight:
			weight[column] = ((weight[column])/total_array)
			
	elif (n_type == 1):
		for column in weight:
			weight[column] = ((weight[column]-mean)/total_array)
	
		
	#print weight
	return weight

def portfoliosharpearima(init_value,final_weight,ln_rt,universe, daterange):
	final_weight_long = final_weight.values
	final_weight_long = final_weight_long.clip(0)
	returns_long_net = ln_rt.values*final_weight_long
	daily_ret_long = np.sum(returns_long_net,axis=1)
	daily_ret_long = pd.DataFrame(daily_ret_long,index = daterange )
	cumulative_ret_long = daily_ret_long.cumsum()
	cumulative_PNL_long = (np.exp(np.array((cumulative_ret_long.values)))-1)*init_value
	pnldf = pd.DataFrame(cumulative_PNL_long, index = daterange, columns = ["PNL"])
	pnldf.plot()
	plt.title("PNL - expected sharpe ratio method")
	plt.xlabel('Date')
	plt.ylabel('PNL in Rs')
	plt.legend(("PNL",))
	plt.savefig("/home/harsha/projects/R/plots/sharpe2.png")
	plt.show()
	
	print "\n\nExpected sharpe ratio forecast performance:"	
	print "Initial investment: Rs {}".format(init_value)
	print "Net PNL: Rs ", pnldf.values[-1]
	print "CAGR = {} %".format((pnldf.values[-1]/init_value)*100)
	print "Sharpe ratio of portfolio(annualized) : {}".format(np.std(np.array(daily_ret_long.values))*pow(246,0.5))
	print "\n\n"	
	


#Load forecast data
forecastarima = load_forecast_data(universe, daterange2)
forecastrnn = pd.read_csv("/home/harsha/projects/R/Project_ideas/rnnforecast/rnnlogreturns.csv", index_col = "Date", parse_dates = True, usecols = ['Date','ICICIBANK', 'BHARTIARTL', 'WIPRO', 'HEROMOTOCO', 'NMDC', 'CIPLA', 'PFC', 'RECLTD','SRTRANSFIN','IDFC', 'DLF', 'CUMMINSIND', 'BRITANNIA', 'MARICO', 'NHPC', 'HINDPETRO', 'BAJAJHLDNG', "SUNDARMFIN", 'JINDALSTEL', 'FEDERALBNK', 'BAYERCROP', 'L&TFH', 'NBCC', 'JUSTDIAL', 'CESC', 'MRPL','MUTHOOTFIN' ], na_values = 'NA' )
#load real returns data
ln_rt = load_real_data(universe,daterange2)
rfr = pd.read_csv("~/projects/R/sharpe/daily_risk_free.csv", index_col = "Date", parse_dates = True, usecols = ['Date','Price'], na_values = 'NA')
rfr =  np.mean(np.array(rfr.values))


weightdfarima = weight(forecastarima,forecastarima.index)
weightdfrnn = weight(forecastrnn,forecastrnn.index)
weightdfsharpe = weightsharpe(forecastarima,forecastarima.index,universe,rfr,ln_rt) 
weightdfsharpe = pd.DataFrame(weightdfsharpe, index = forecastarima.index, columns = forecastarima.columns).dropna()

final_weightarima = neutralize(weightdfarima,0,universe,forecastarima.index)
final_weightrnn = neutralize(weightdfrnn,0,universe,forecastrnn.index)
final_weightsharpe = neutralize(weightdfsharpe,0,universe,forecastarima.index)
	
#portfolioarma(init_value,final_weightarima,ln_rt,universe, final_weightarima.index)

#portfoliornn(init_value,final_weightrnn,ln_rt,universe, final_weightrnn.index)

portfoliosharpearima(init_value,final_weightsharpe,ln_rt,universe, final_weightarima.index)

	
