"""
This script contains the core and auxiliary functions for the calculation
"""
import yfinance as yf
import pandas_datareader as pdr
#This override is neccessarry to overcome the data limitations of yahoo finance
yf.pdr_override()
import datetime as dt
from pandas.tseries.offsets import BDay
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import urllib
from time import perf_counter
import plotly.express as px
import sklearn
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt

#Decorators

def timed(fn):
    """This functions times the execution of the inpit function

    Args:
        fn (function): Any selected function for whichh timing exercise needs to be performed

    Returns:
        Inner function: _returns the inputted functions wrapped with the timining functionality
    """
    from functools import wraps
    from datetime import datetime, timezone
    from time import perf_counter

    @wraps(fn)
    def inner(*args, **kwargs):
        start= perf_counter()
        result=fn(*args,**kwargs)
        end=perf_counter()
        print('{0} ran for {1:.6f}s'.format(fn.__name__, end-start))
        return result
    return inner

#Classes

#functions
def comparison_scatter_plotting_duo(X1,X2,Y,target_names,colors, title1, title2, mainTitle, ShowPlot:bool= True):
    """This function plots duo scatterplots from calibrated model outputs

    Args:
        X1 (_type_): _description_
        X2 (_type_): _description_
        Y (_type_): Target variable of the population
        target_name (_type_): _description_
        colors (_type_): _description_
        ShowPlot (bool, optional): _description_. Defaults to True.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(mainTitle)

    colors = ["#E74C3C", "#3498DB", "#D4AC0D"]
    lw = 2
    #PCA
    #ax1.figure()
    for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        ax1.scatter(
            X1[Y== i, 0], X1[Y == i, 1], color=color, alpha=0.8, lw=lw, label=target_name
        )
    ax1.legend(loc="best", shadow=False, scatterpoints=1)
    ax1.set_title(title2)
    #LDA
    #ax2.figure()
    for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        ax2.scatter(
            X2[Y == i, 0], X2[Y == i, 1], alpha=0.8, color=color, label=target_name
        )
    ax2.legend(loc="best", shadow=False, scatterpoints=1)
    ax2.set_title(title2)

    if (ShowPlot):
        fig.show()
    return(fig)

def get_security_yahoofinance(ticker, period, columns):
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

def get_security_pandas_datareader(ticker, start, end, column_to_display):
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
    downloaded= pdr.data.DataReader(ticker, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    close=downloaded.loc[:,downloaded.columns.isin([column_to_display], level=0)]
    close = close.fillna(method='ffill')
    if isinstance(close.columns, pd.MultiIndex):
        close.columns=close.columns.get_level_values(1)
    # Getting all weekdays between star and enddate
    all_weekdays = pd.date_range((start+BDay(2)).strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), freq='B')
    close = close.reindex(all_weekdays)
    return(close)

def calculate_returns(is_logreturn,data,days_lag, Notional):
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
    #df_index=pd.DataFrame(columns=data.columns, index=data.index).fillna(value=100)
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

def calculate_summary_stat(data):
    loss_quantile=0.995
    return_quantile =np.quantile(data,loss_quantile)
    return(return_quantile)

def show_box_plots_of_returns(data):
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

def show_return_time_series(data):
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
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        ),
                    yaxis= dict(
                            showgrid=False,
                            showline=True,
                            showticklabels=True,
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

def show_portfolio_evolution(data):
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
    colorpalette=px.colors.sequential.Bluyl
    for idx, col in enumerate(data.columns, 0):
        fig.add_trace(go.Scatter(x=data.index,
                            y=data.iloc[:,idx],#data[data.columns[0]],
                            #color=volumes[data.columns[0]],
                            mode='lines',
                            line=dict(
                                width=0.5,
                                color=colorpalette[idx]
                            ),
                            stackgroup='one',
                            #marker_size = volumes[data.columns[0]],
                            name=col))#data.columns[0]))
    fig.update_layout(paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    #margin=dict(l=2,r=2,b=2,t=2),
                    title="Portfolio value evolution over time",
                    xaxis= dict(
                        title="Date",
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        ),
                    yaxis= dict(
                            showgrid=False,
                            showline=True,
                            showticklabels=True,
                            title="Value of the portfolio",
                        ),
                    font= dict(
                        family="Helvetica",
                        size=16,
                        color='#2B2C2E',
                    )
                )
    return(fig)

