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
google_api_key = "AIzaSyCVMnMLqp6EWFZYeW5kl-wYm6nVOl-TxKg"
client = RESTClient(api_key)


mktData = pd.DataFrame(client.get_grouped_daily_aggs(date='2023-04-13', include_otc=True, locale='us'))
tickerList = list(mktData.ticker)

st.title('Stock Viewer')
ticker = st.sidebar.selectbox('Symbol', options= tickerList) #e.g MSFT, AAPL, TSLA
start_date = st.sidebar.date_input('Start Date', datetime.date(2022, 4, 1))
end_date = st.sidebar.date_input('End Date', datetime.date(2023, 4, 1))
tickerInfo = yf.Ticker(ticker)
#tickerInfo.info
string_name = tickerInfo.info['longName']
st.subheader('**%s**' % string_name)


data = yf.download(ticker, start=start_date, end=end_date)
data
fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)
figure = go.Figure(
    data = [
            go.Candlestick(
                x = data.index,
                low=data['Low'],
                high = data['High'],
                close= data['Close'],
                open= data['Open'],
                increasing_line_color = 'green',
                decreasing_line_color = 'red'
            )
    ]
)
figure.update_layout(title = ticker, yaxis_title = 'Adj Close')
st.plotly_chart(figure)
check = st.checkbox('View company summary')
if check:
    st.subheader("Company Summary")
    tickerSummary = tickerInfo.info['longBusinessSummary']
    st.info(tickerSummary)
address1 = tickerInfo.info['address1']
city = tickerInfo.info['city']
state = tickerInfo.info['state']
zip = tickerInfo.info['zip']
address = [address1, city, state, zip]
address2 = [city, state, zip]


if st.button('Display Map'):
    st.subheader("Company Location")
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(timeout=10)
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude
        m = folium.Map(location=[latitude, longitude], zoom_start=10)
        folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)
        folium_static(m)
    except:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(address2)
        latitude = location.latitude
        longitude = location.longitude
        m = folium.Map(location=[latitude, longitude], zoom_start=10)
        folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)
        folium_static(m)



st.success('Stock information displayed.')


