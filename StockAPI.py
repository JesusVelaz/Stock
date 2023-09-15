import datetime
import folium
from streamlit_folium import folium_static
import urllib.parse
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from polygon import RESTClient
api_key = "RD13r6x2InhRuNkiR47R8SRuknxUCPya"
client = RESTClient(api_key)

mktData = pd.DataFrame(client.get_grouped_daily_aggs(date='2023-04-13', include_otc=True, locale='us'))
tickerList = list(mktData.ticker)

st.title('Stock Viewer')
ticker = st.sidebar.selectbox('Symbol', options= tickerList) #e.g MSFT, AAPL, TSLA symbol
tickerInfo = yf.Ticker(ticker)

start_date = st.sidebar.date_input('Start Date', datetime.date(2022, 4, 1))
end_date = st.sidebar.date_input('End Date', datetime.date(2023, 4, 1))


data = yf.download(ticker, start=start_date, end=end_date)


if data.empty:
    st.error("No data available for the selected ticker symbol.")
else:
    # Display stock information
    st.subheader(f'Stock Information for {ticker}')
    st.write(data)

    # Create and display a line chart
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=f'{ticker} Stock Price')
    st.plotly_chart(fig)

    # Create and display a candlestick chart
    fig_candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                                                     open=data['Open'],
                                                     high=data['High'],
                                                     low=data['Low'],
                                                     close=data['Close'],
                                                     increasing_line_color='green',
                                                     decreasing_line_color='red')])
    fig_candlestick.update_layout(title=f'{ticker} Candlestick Chart', yaxis_title='Price')
    st.plotly_chart(fig_candlestick)


st.success('Stock information displayed.')


