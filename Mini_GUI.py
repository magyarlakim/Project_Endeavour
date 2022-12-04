from tkinter import *
from tkhtmlview import HTMLLabel
import Aux_functions as aux
import datetime as dt
import numpy as np

def callback():
    print('button clicked n times!')
    result_field.configure(text = str(entry_field.get())+"You have selected " + str(number_scale.get()) +" securities!")

def Fetch_securites():

    try:
        ticker=[str(entry_field.get())]
        quantile=float(number_scale.get())/100
        #ticker=['CSGN.SW']
        start=dt.datetime(2019,1,1)
        end=dt.datetime(2022,12,2)
        column_to_display='Adj Close'
        days_lag=5
        #Get the closing prices and the volumes
        ClosePrice=aux.Get_security_pandas_datareader(ticker, start, end, column_to_display)
        daily_log, daily_index=aux.Calculate_returns(is_logreturn=True, data=ClosePrice, days_lag=days_lag, Notional=100)
        daily_log=daily_log.fillna(method='ffill')
        #np.average(daily_log[ticker].values)
        #aux.Calculate_summary_stat(data)
        loss_quantile=1-quantile
        return_portfolio =np.quantile(daily_log[ticker].values,loss_quantile)
        result_field.configure(text = "The "+str("%.2f" %loss_quantile)+
        " Quantile of the return distribution for the selected security is as follows: " + str("%.2f" %return_portfolio) +"% !")
    except:
        result_field.configure(text = "Please put in an existing ticker on Yahoo and try again!")
# Create Object
root = Tk()
root.title("PSE mini: The Portfolio Selector Engine")
img = PhotoImage(file='static/img/Jungle.png')
canvas = Canvas(
    root,
    width = 500, 
    height = 100,
    )      
  
# Set Geometry
root.geometry("600x400")
text="Click me!"
# Add label
canvas.pack()
canvas.create_image(
    0,
    0,
    anchor=NW,
    image=img
)
info_label=Label(root, text="Please provide the ticker!").pack()
entry_field=Entry(root)
entry_field.pack()

info_label2=Label(root, text="Please provide the quantile for which you would like to calculate the metric!").pack()
number_scale=Scale(root, from_=90, to=100, length=300, tickinterval=0.5, orient=HORIZONTAL)
number_scale.pack()
calc_button=Button(root, text=text, command=Fetch_securites)
result_field=Label(root)
# Adjust label
calc_button.pack(pady=20, padx=20)
result_field.pack()
 
 
# Execute Tkinter
root.mainloop()