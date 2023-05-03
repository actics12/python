#!/usr/bin/env python
# coding: utf-8

# 23/4/30 start, endを固定化

# In[1]:

from pandas_datareader import data as pdr
import openpyxl
import talib as ta
import datetime
import yfinance as yf 
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


# In[9]:


def F_BACKTESTING(ticker):
    
    yf.pdr_override()
    end = datetime.date.today()
    start = end - datetime.timedelta(days=400)
    data = pdr.get_data_yahoo(ticker, start, end, interval = '1wk')
    
    class SmaCross(Strategy):
        Ns1 = 10 # 短期SMA
        Ns2 = 30 # 長期SMA

        def init(self):
            self.sma1 = self.I(SMA, self.data.Close, self.Ns1) 
            self.sma2 = self.I(SMA, self.data.Close, self.Ns2)

        def next(self): #チャートデータの行ごとに呼び出される
            if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
                self.buy() # 買い
            elif crossover(self.sma2, self.sma1):
                self.position.close()
    
    bt_SMA = Backtest(
    data, # チャートデータ
    SmaCross, # 売買戦略
    cash=100000, # 最初の所持金
    commission=0.00495, # 取引手数料
    margin=1.0, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
    trade_on_close=False, # True：現在の終値で取引，False：次の時間の始値で取引
    exclusive_orders=True #自動でポジションをクローズ
)

    output_SMA=bt_SMA.optimize(Ns1=range(10, 50, 1), Ns2=range(10, 50, 1), maximize='Equity Final [$]', constraint=lambda p: p.Ns1 < p.Ns2)
#    output_SMA=bt_SMA.optimize(Ns1=range(10, 13, 1), Ns2=range(10, 13, 1), maximize='Equity Final [$]', constraint=lambda p: p.Ns1 < p.Ns2)


#短期、長期移動平均日数の取得
    s = str(output_SMA._strategy)
    first = s.find('Ns1=') + len('Ns1=')
    final = s.find(',', first)
    SMA_short = int(s[first:final])

    first = s.find('Ns2=') + len('Ns2=')
    final = s.find(')', first)
    SMA_long = int(s[first:final])

#以上SMA
    
    def MACD(close, Nm1, Nm2, Nms):
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod=Nm1, slowperiod=Nm2, signalperiod=Nms)
        return macd, macdsignal
    
    class MACDCross(Strategy):
        Nm1 = 12 #短期EMAの期間
        Nm2 = 26 #長期EMAの期間
        Nms = 9 #シグナル（MACDのSMA）の期間

        def init(self):
            self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.Nm1, self.Nm2, self.Nms)

        def next(self): # チャートデータの行ごとに呼び出される
            if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
                self.buy() # 買い
            elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
                self.position.close() # 売り
                    
    bt_MACD = Backtest(
        data, # チャートデータ
        MACDCross, # 売買戦略
        cash=100000, # 最初の所持金
        commission=0.00495, # 取引手数料
        margin=1.0, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
        trade_on_close=True, # True：現在の終値で取引，False：次の時間の始値で取引
        exclusive_orders=True #自動でポジションをクローズ
    )

#最適化
    output_MACD=bt_MACD.optimize(Nm1=range(10, 50, 1),Nm2=range(10, 50, 1), Nms=range(3,30,1))
#    output_MACD=bt_MACD.optimize(Nm1=range(10, 13, 1),Nm2=range(10, 13, 1), Nms=range(10,11,1))
        
#短期、長期移動平均日数の取得
    s = str(output_MACD._strategy)
    first = s.find('Nm1=') + len('Nm1=')
    final = s.find(',', first)
    EMA_short = int(s[first:final])

    first = s.find('Nm2=') + len('Nm2=')
    final = s.find(',', first)
    EMA_long = int(s[first:final])
    
    first = s.find('Nms=') + len('Nms=')
    final = s.find(')', first)
    signal = int(s[first:final])  
    
    result_df = pd.DataFrame({'SMA_short': [SMA_short], 'SMA_long': [SMA_long], 'EMA_short' : [EMA_short], 'EMA_long' : [EMA_long], 'signal' : [signal]})
    
    output_SMA.index = output_SMA.index.astype(str)
    output_MACD.index = output_MACD.index.astype(str)
    
    with pd.ExcelWriter(f'{ticker}output.xlsx') as writer:  # Excelファイルを開く
        output_SMA.to_excel(writer, sheet_name='Sheet1', index=False)  # 1つ目のデータフレームを書き出す
        output_MACD.to_excel(writer, sheet_name='Sheet2', index=False)  # 2つ目のデータフレームを書き出す
        result_df.to_excel(writer, sheet_name='Sheet3', index=False)  # 3つ目のデータフレームを書き出す


# In[7]:


tickers = ['VHI', 'VHT', 'VTI', 'VFH', 'VDE', 'VDC', 'VCR']
for ticker in tickers:
    F_BACKTESTING(ticker)



# In[ ]:




