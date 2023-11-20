# import useful libraries
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.express as px

# Dashboard Title
st.markdown('<h1 style="text-align:center">Stock Dashboard</h1>', unsafe_allow_html=True)
st.markdown('---', unsafe_allow_html=True)

# sidebar
ticker = st.sidebar.text_input('Enter ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# extract yahoo finance data
data = yf.download(ticker, start=start_date, end=end_date)

# plot close line graph
closing_stock_graph = px.line(data, x=data.index, y=data['Close'], title=ticker)
st.plotly_chart(closing_stock_graph)

# create tabs for pricing data,fundamental data and top ten news
st.markdown('---', unsafe_allow_html=True)
pricing_data, fundamental_data, news = st.tabs(['Pricing Data', 'Fundamental Data', 'Top 10 news'])

with pricing_data:
    # annual returns and percentage change
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Close'] / data['Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_returns = data2['% Change'].mean() * 252 * 100
    st.write('Annual Returns is:', annual_returns, "%")

    # standard deviation
    standard_dev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is:', standard_dev)

# fundamental data section
from alpha_vantage.fundamentaldata import FundamentalData

with fundamental_data:
    key = ""
    fd = FundamentalData(key, output_format='pandas')

    # get balance sheet
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])

    # get income statement
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    ist = income_statement.T[2:]
    ist.columns = list(income_statement.T.iloc[0])
    st.write(ist)

    # get cash flow
    st.subheader('Cash Flow')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)


# news tab
from stocknews import StockNews
with news:
    st.subheader(f'News of {ticker}')
    sn=StockNews(ticker,save_news=False)
    df_news=sn.read_rss()
    for i in range(10):
        st.subheader(f'News of {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment=df_news['sentiment_title'][i]
        st.write(f'Title Sentiment{title_sentiment}')
        news_sentiment=df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

