#!/usr/bin/env python
# coding: utf-8

# 2023/4/29　関数名を大文字化、リストにしてfor文化、
# 2023/4/30　パラメータを自動取得化

# In[1]:


import yfinance as yf
import pandas_datareader.data as pdr
import datetime
import pandas as pd
from datetime import timedelta


# In[2]:


def ETF_PRICE_DATA(ticker, SMA_short, SMA_long, EMA_short, EMA_long, signal):
    
        
    start = datetime.date(2010, 9, 1)
    end = datetime.date.today()
    yf.pdr_override()
    df = pdr.get_data_yahoo(ticker, start, end)
    df.index = df.index.tz_localize(None)
    
    #SMA
    df['SMA_short'] = df['Close'] .rolling(window=SMA_short).mean()
    df['SMA_long'] =df['Close'].rolling(window=SMA_long).mean()
    
    #MACD
    
    df['EMA_short'] = df['Close'].ewm(span=EMA_short).mean()
    df['EMA_long'] = df['Close'].ewm(span=EMA_long).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['signal'] = df['MACD'].ewm(span=signal).mean()
    df['diff'] = df['MACD'] - df['signal']
    f_plus = lambda x: x if x > 0 else 0
    f_minus = lambda x: x if x < 0 else 0
    df['diff+'] = df['diff'].map(f_plus)
    df['diff-'] = df['diff'].map(f_minus)
    
    df = df.reset_index()
    df['Date'] = df['Date'].astype(str)
#    df['Date'] = df['Date'].apply(lambda a: datetime.datetime.strftime(a,"%Y-%m-%d %H:%M:%S"))
    
    df.to_excel(f"{ticker}_Stock_Price_Data.xlsx", index = False)
        


# In[34]:


tickers = ['VHI', 'VHT', 'VTI', 'VFH', 'VDE', 'VDC', 'VCR']


# In[38]:


params = []
for ticker in tickers:
    df_params = pd.read_excel(f"C:/Users/actic/OneDrive/10_株式投資/python_本番環境/株バックテスト/pycharm/{ticker}output.xlsx", sheet_name = 'Sheet3')
    list = df_params.iloc[0].tolist()
    params.append(tuple(list))
params


# In[40]:


print(f'start:{datetime.datetime.now()}')
for i, ticker in enumerate(tickers):
    p = params[i]
    ETF_PRICE_DATA(ticker, p[0], p[1], p[2], p[3], p[4])
print(f'finish:{datetime.datetime.now()}')


# In[ ]:





# In[ ]:




