"""
This script is responsible for calculating concentration on a given entropy
"""
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from math import pi
import urllib
from time import perf_counter
import yfinance as yf
import pandas_datareader as pdr
import datetime as dt
from pandas.tseries.offsets import BDay
import Aux_functions as aux
from importlib import reload
reload(aux)

# Inputs for datafetching and portfolio visualization
ticker=['AAPL','^GSPC','MS','MSFT','EBS.VI','MOL.BD','CSGN.SW']
start=dt.datetime(2019,1,1)
end=dt.datetime(2022,12,2)
column_to_display='Adj Close'
days_lag=5


#Get the closing prices and the volumes
ClosePrice=aux.Get_security_pandas_datareader(ticker, start, end, column_to_display)
Volumes=aux.Get_security_pandas_datareader(ticker, start, end, column_to_display="Volume")
daily_log, daily_index=aux.Calculate_returns(is_logreturn=True, data=ClosePrice, days_lag=days_lag, Notional=100)
daily_index
volumes=Volumes.iloc[days_lag:,:]
Portfolio_img=aux.Show_return_time_series(daily_index)
Portfolio_img.show()
aux.Show_box_plots_of_returns(daily_log)
daily_index