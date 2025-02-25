import pandas as pd 
from alpha_vantage.timeseries import TimeSeries

API_key = 'R1YZD9FC9ZEA5QNO' 
def get_API_key(): 
    return API_key 

def get_moving_average(API_key, ticker, days_in_period, num_periods):
    
        try:
# initialize Alpha Vantage TimeSeries object
            ts = TimeSeries(key=API_key, output_format='pandas')

    # fetch daily stock data
            data, _ = ts.get_daily(symbol=ticker, outputsize='full')
            data = data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

    # sort data by date
            data = data.sort_index()
            
        # error handling
            total_days = days_in_period + num_periods - 1
            if len(data) < total_days:
                return f"Not enough data available. The stock only has {len(data)} days of data, " \
                   f"but {total_days} days are required for the calculation."

    # calculate moving average
            data['Moving Average'] = data['Close'].rolling(window=days_in_period).mean()

    # extract the last "num_periods" moving average values
            moving_average_values = data['Moving Average'].dropna().tail(num_periods).tolist()
            return moving_average_values
        
        except Exception as e:
            return f"An error occurred: {e}"


    


    





"""
import requests
response = requests.get('https://api.github.com')
print(response.status_code)
""" 