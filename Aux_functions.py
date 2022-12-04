"""
This script contains the auxiliary functions for the calculation
"""
import yfinance as yf
import pandas_datareader as pdr
import datetime as dt
from pandas.tseries.offsets import BDay
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import urllib
from time import perf_counter
import plotly.express as px
import plotly.offline.plot as ploff

def Get_security_Yahoofinance(ticker, period, columns):
    """
    Function to fetch security data from yahoo finance directly
    though yahoofinance package
    Input:
        ticker: tickers for security desired
        period: 1d,5d,10d, 1m, max
        columns: columns that one wishes to obtain
    Output:
        Dataframe with results
    """
    security_object=yf.Ticker(ticker)
    Output=security_object.history(period=period)[columns]
    return(Output)

def Get_security_pandas_datareader(ticker, start, end, column_to_display):
    """
    Function to fetch security data from yahoo finance directly
    though yahoofinance package
    Input:
        ticker: tickers for security desired
        period: 1d,5d,10d, 1m, max
        columns: columns that one wishes to obtain
    Output:
        Dataframe with results
    """
    downloaded= pdr.data.DataReader(ticker,'yahoo', start, end)
    close=downloaded.loc[:,downloaded.columns.isin([column_to_display], level=0)]
    close = close.fillna(method='ffill')
    close.columns=close.columns.get_level_values(1)
    # Getting all weekdays between star and enddate
    all_weekdays = pd.date_range(start+BDay(2), end, freq='B')
    close = close.reindex(all_weekdays)
    return(close)

def Calculate_returns(is_logreturn,data,days_lag, Notional):
    """
    Create log or normal return dataframes
    Input:
        is_logreturn: boolean Variable
        data: dataframe consisting of prices organised in columns
        days_lag: actual shift in days used to calculate returns
        Notional is the initinal investment on each security

    Output:
        Returns of the securities specified
    """
    df_index=pd.DataFrame(columns=data.columns, index=data.index).fillna(value=100)
    if (is_logreturn):
        print("calculating logreturns with "+str(days_lag)+" day shift!")
        #calculate normal returns and select only every nth element to refelct the true return as a time series
        df_returns=np.log(data/data.shift(days_lag))
        df_returns=df_returns.iloc[days_lag::days_lag,:]
        df_index= np.exp(np.cumsum(df_returns.shift(1)))*Notional

    else:
        print("calculating normal returns with "+str(days_lag)+" day shift!")
        #calculate normal returns and select only every nth element to refelct the true return as a time series
        df_returns=(data/data.shift(days_lag))-1
        df_returns=df_returns.iloc[days_lag::days_lag,:]
        df_index=np.cumproduct(1+df_returns)*Notional
    #generic formatting to remove leading NAs from dataframe
   
    df_index=df_index.iloc[days_lag:,:]
    return(df_returns, df_index)

def Calculate_summary_stat(data):
    
    return()
def Show_box_plots_of_returns(data):
    """
    This function shows box plots of return data for multiple securities

    Input:
        data: Contains a dataframe where columns are the security tickers and
        rows are return observation at a point of time
    Output:
        Plotly plot of multiple box and whiskers plotfor multiple securities
    """
    
    fig = go.Figure()
    colorpalette=px.colors.sequential.Plasma
    for idx, col in enumerate(data.columns, 0):
        fig.add_trace(go.Box(y=data.iloc[:,idx],
                        name=col,
                        marker_color=colorpalette[idx]))
        fig.update_layout(paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    #margin=dict(l=2,r=2,b=2,t=2),
                    title="Return distribution of portfolio constituents",
                    xaxis= dict(
                        
                        showgrid=False,
                        ),
                    yaxis= dict(showgrid=True,
                            
                        ),
                    font= dict(
                        family="Helvetica",
                        size=16,
                        color='#2B2C2E',
                    )
                )
    fig.show()

def Show_return_time_series(data):
    """
    This function shows time series of data for multiple securities

    Input:
        data: Contains a dataframe where columns are the security tickers and
        rows are return observation at a point of time
    Output:
        Plotly plot of multiple time series of underlying portfolio components
    """
    # Create figure with iterative multiple lines
    fig = go.Figure()
    colorpalette=px.colors.sequential.Plasma
    for idx, col in enumerate(data.columns, 0):
        fig.add_trace(go.Scatter(x=data.index,
                            y=data.iloc[:,idx],#data[data.columns[0]],
                            #color=volumes[data.columns[0]],
                            # mode='markers',
                            marker=dict(
                                 color=colorpalette[idx],#volumes.iloc[:,idx],#[data.columns[0]],
                            #     colorscale="Viridis"
                             ),
                            #marker_size = volumes[data.columns[0]],
                            name=col))#data.columns[0]))
    fig.update_layout(paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    #margin=dict(l=2,r=2,b=2,t=2),
                    title="Price evolution of portfolio constituents",
                    xaxis= dict(
                        title="Date",
                        showgrid=False,
                        ),
                    yaxis= dict(showgrid=True,
                            title="Value of 100 unit investment",
                        ),
                    font= dict(
                        family="Helvetica",
                        size=16,
                        color='#2B2C2E',
                    )
                )
    #fig.show(output_type='div')
    return(fig)
# Playing around with classes

class Paramount():
    """ A usefull class to start with
    :inpu1= Nothing
    :input2= Nothing again
    :outout= Nothing
    """
    language= 'Turkish'
    version='1.1'
    def say_hello():
        print(f'Hello from{Paramount.language}')


class Circle:
    """ This class is using property and cahcing the value """
    def __init__(self, radius):
        self._radius = radius
        self._area = None
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._area = None
        self._radius = value
    
    @property
    def area(self):
        if self._area is None:
            print('Calculating area')
            self._area = np.pi * (self.radius ** 2)
        return self._area


c= Circle(1)
c.area
c.radius = 2
c.__dict__
c.area

class WebPage:
    def __init__(self, url):
        self.url = url
        self._page= None
        self._load_time_secs = None
        self._page_size = None

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        self._page = None
    
    @property
    def page(self):
        if self._page is None:
            self.download_page()
        return self._page
    
    @property
    def page_size(self):
        if self._page is None:
            self.download_page()
        return self._page_size

    @property
    def time_elapsed(self):
        if self._page is None:
            self.download_page()
        return self._load_time_secs
    
    def download_page(self):
        self._page_size=None
        self._load_time_secs = None
        start_time = perf_counter()
        with urllib.request.urlopen(self.url) as f:
            self._page=f.read()
        end_time= perf_counter()
        self._load_time_secs= end_time- start_time

urls = [
    'https://wwww.google.com',
    'https://wwww.python.org',
    'https://wwww.yahoo.com'
]

#for url in urls:
#    page=WebPage(url)
#    print(f'{url}\tsize={format(page.page_size, "_")}\telapsed={page.time_elapsed:.2f} secs')
    